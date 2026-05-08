import uuid

from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import delivery_photo as crud_photo
from app.models.user import User

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024


class DeliveryPhotoService:
    async def get_route_photos(self, db: AsyncSession, route_id: int):
        return await crud_photo.get_photos_by_route(db, route_id)

    async def upload_photo(
        self,
        db: AsyncSession,
        route_id: int,
        file: UploadFile,
        description: str | None,
        current_user: User,
    ):
        self._validate_file(file)

        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400, detail="File size exceeds 10 MB limit"
            )

        key = self._generate_key(route_id, file.filename)

        photo = await crud_photo.create_photo(db, route_id, key, description)

        url = self._build_url(key)
        return {"key": photo.key, "url": url}

    def _validate_file(self, file: UploadFile):
        if file.content_type not in ALLOWED_CONTENT_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: "
                f"{', '.join(ALLOWED_CONTENT_TYPES)}",
            )

    def _generate_key(self, route_id: int, filename: str) -> str:
        ext = filename.rsplit(".", 1)[-1] if "." in filename else "jpg"
        return f"delivery_photos/route_{route_id}/{uuid.uuid4()}.{ext}"

    def _build_url(self, key: str) -> str:
        return f"https://your-bucket.s3.amazonaws.com/{key}"


delivery_photo_service = DeliveryPhotoService()
