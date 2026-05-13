from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.invoice import Invoice
from app.schemas.invoice import InvoiceCreate, InvoiceUpdate


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
