from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.db.deps import get_db
from backend.schemas.asset_schema import AssetCreate, AssetUpdate, AssetOut
from backend.services.asset_service import (
    get_assets, get_asset, create_asset,
    update_asset, delete_asset
)

router = APIRouter(prefix="/assets", tags=["Assets"])

@router.get("/", response_model=List[AssetOut])
def read_assets(db: Session = Depends(get_db)):
    return get_assets(db)

@router.get("/{asset_id}", response_model=AssetOut)
def read_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = get_asset(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset

@router.post("/", response_model=AssetOut)
def add_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    return create_asset(db, asset)

@router.put("/{asset_id}", response_model=AssetOut)
def edit_asset(asset_id: int, asset: AssetUpdate, db: Session = Depends(get_db)):
    updated = update_asset(db, asset_id, asset)
    if not updated:
        raise HTTPException(status_code=404, detail="Asset not found")
    return updated

@router.delete("/{asset_id}", response_model=AssetOut)
def remove_asset(asset_id: int, db: Session = Depends(get_db)):
    deleted = delete_asset(db, asset_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Asset not found")
    return deleted
