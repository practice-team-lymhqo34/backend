from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import invoice as crud_invoice
from app.schemas.invoice import InvoiceCreate, InvoiceUpdate


class InvoiceService:
    async def get_invoice_or_404(self, db: AsyncSession, invoice_id: int):
        invoice = await crud_invoice.get_invoice_by_id(db, invoice_id)
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        return invoice

    async def get_invoices(self, db: AsyncSession, **filters):
        return await crud_invoice.get_invoices(db, **filters)

    async def create_invoice(
        self, db: AsyncSession, invoice_in: InvoiceCreate
    ):
        return await crud_invoice.create_invoice(db, invoice_in)

    async def update_invoice(
        self,
        db: AsyncSession,
        invoice_id: int,
        invoice_in: InvoiceUpdate,
    ):
        invoice = await self.get_invoice_or_404(db, invoice_id)
        return await crud_invoice.update_invoice(db, invoice, invoice_in)

    async def delete_invoice(self, db: AsyncSession, invoice_id: int):
        invoice = await self.get_invoice_or_404(db, invoice_id)
        await crud_invoice.delete_invoice(db, invoice)

    async def get_monthly_statistics(
        self, db: AsyncSession, owner_id: Optional[int] = None
    ):
        return await crud_invoice.get_monthly_statistics(db, owner_id)


invoice_service = InvoiceService()
