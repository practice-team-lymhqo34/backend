from typing import Optional, Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.invoice import Invoice
from app.schemas.invoice import (
    InvoiceCreate,
    InvoiceUpdate,
    MonthlyExpenseStat,
)


async def get_invoice_by_id(
    db: AsyncSession, invoice_id: int
) -> Optional[Invoice]:
    result = await db.execute(select(Invoice).where(Invoice.id == invoice_id))
    return result.scalars().first()


async def get_invoices(
    db: AsyncSession,
    owner_id: Optional[int] = None,
) -> Sequence[Invoice]:
    query = select(Invoice)
    if owner_id is not None:
        query = query.where(Invoice.owner_id == owner_id)
    result = await db.execute(query)
    return result.scalars().all()


async def create_invoice(
    db: AsyncSession, invoice_in: InvoiceCreate
) -> Invoice:
    db_invoice = Invoice(**invoice_in.model_dump())
    db.add(db_invoice)
    await db.commit()
    await db.refresh(db_invoice)
    return db_invoice


async def update_invoice(
    db: AsyncSession, invoice: Invoice, invoice_in: InvoiceUpdate
) -> Invoice:
    update_data = invoice_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(invoice, field, value)
    db.add(invoice)
    await db.commit()
    await db.refresh(invoice)
    return invoice


async def delete_invoice(db: AsyncSession, invoice: Invoice) -> None:
    await db.delete(invoice)
    await db.commit()


async def get_monthly_statistics(
    db: AsyncSession, owner_id: Optional[int] = None
) -> Sequence[MonthlyExpenseStat]:
    month_col = func.date_trunc("month", Invoice.billing_month).label("month")

    query = (
        select(
            month_col,
            func.sum(Invoice.total_shipment).label("total_shipments"),
            func.sum(Invoice.total_weight).label("total_weight"),
            func.sum(Invoice.total_volume).label("total_volume"),
            func.sum(Invoice.total_distance).label("total_distance"),
            func.count(Invoice.id).label("invoice_count"),
        )
        .group_by("month")
        .order_by(month_col.desc())
    )

    if owner_id is not None:
        query = query.where(Invoice.owner_id == owner_id)

    result = await db.execute(query)
    return [
        MonthlyExpenseStat(
            month=row.month,
            total_shipments=row.total_shipments or 0,
            total_weight=float(row.total_weight or 0),
            total_volume=float(row.total_volume or 0),
            total_distance=float(row.total_distance or 0),
            invoice_count=row.invoice_count,
        )
        for row in result.all()
    ]
