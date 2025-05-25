from sqlalchemy.orm import Session
from backend.models.asset_model import Asset
from backend.schemas.asset_schema import AssetCreate, AssetUpdate

def get_assets(db: Session):
    return db.query(Asset).all()

def get_asset(db: Session, asset_id: int):
    return db.query(Asset).filter(Asset.id == asset_id).first()

def create_asset(db: Session, asset: AssetCreate):
    db_asset = Asset(**asset.dict())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

def update_asset(db: Session, asset_id: int, asset: AssetUpdate):
    db_asset = get_asset(db, asset_id)
    if db_asset is None:
        return None
    for key, value in asset.dict().items():
        setattr(db_asset, key, value)
    db.commit()
    db.refresh(db_asset)
    return db_asset

def delete_asset(db: Session, asset_id: int):
    db_asset = get_asset(db, asset_id)
    if db_asset is None:
        return None
    db.delete(db_asset)
    db.commit()
    return db_asset
