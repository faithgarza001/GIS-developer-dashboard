from pydantic import BaseModel

class AssetBase(BaseModel):
    name: str
    type: str

class AssetCreate(AssetBase):
    pass

class AssetUpdate(AssetBase):
    pass

class AssetOut(AssetBase):
    id: int

    class Config:
        orm_mode = True
