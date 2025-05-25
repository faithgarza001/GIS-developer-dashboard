from sqlalchemy.orm import Session
from backend.models.file_upload_model import GeoFileUpload
from backend.schemas.file_upload_schema import FileUploadCreate

def save_file_upload(db: Session, file_data: FileUploadCreate):
    db_upload = GeoFileUpload(**file_data.dict())
    db.add(db_upload)
    db.commit()
    db.refresh(db_upload)
    return db_upload

def get_all_uploads(db: Session):
    return db.query(GeoFileUpload).all()
