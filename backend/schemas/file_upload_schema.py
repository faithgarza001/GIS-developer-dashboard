from pydantic import BaseModel
from datetime import datetime

class FileUploadBase(BaseModel):
    filename: str
    feature_count: int
    geometry_type: str

class FileUploadCreate(FileUploadBase):
    pass

class FileUploadOut(FileUploadBase):
    id: int
    uploaded_at: datetime

    class Config:
        orm_mode = True
