from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.db.deps import get_db
from backend.schemas.file_upload_schema import FileUploadCreate, FileUploadOut
from backend.services.file_upload_service import save_file_upload, get_all_uploads

import json
import zipfile
import os
import tempfile
import fiona

router = APIRouter(prefix="/files", tags=["Files"])

@router.post("/upload", response_model=FileUploadOut)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    filename = file.filename.lower()
    contents = await file.read()

    # --- Handle GeoJSON Upload ---
    if filename.endswith(".geojson"):
        try:
            # Save file to uploads/
            os.makedirs("uploads", exist_ok=True)
            file_path = os.path.join("uploads", file.filename)
            with open(file_path, "wb") as f:
                f.write(contents)

            geojson_data = json.loads(contents.decode("utf-8"))
            feature_count = len(geojson_data.get("features", []))
            geom_type = geojson_data["features"][0]["geometry"]["type"] if feature_count > 0 else "Unknown"

            file_data = FileUploadCreate(
                filename=file.filename,
                feature_count=feature_count,
                geometry_type=geom_type
            )
            return save_file_upload(db, file_data)

        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Invalid GeoJSON: {str(e)}")

    # --- Handle .shp.zip Upload ---
    elif filename.endswith(".zip"):
        try:
            temp_dir = tempfile.mkdtemp()
            zip_path = os.path.join(temp_dir, filename)

            with open(zip_path, "wb") as f:
                f.write(contents)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            shp_files = [f for f in os.listdir(temp_dir) if f.endswith(".shp")]
            if not shp_files:
                raise HTTPException(status_code=422, detail="No .shp file found in the ZIP.")

            shp_path = os.path.join(temp_dir, shp_files[0])

            with fiona.open(shp_path, "r") as src:
                feature_count = len(src)
                geom_type = src.schema["geometry"]

            file_data = FileUploadCreate(
                filename=file.filename,
                feature_count=feature_count,
                geometry_type=geom_type
            )
            return save_file_upload(db, file_data)

        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Invalid Shapefile: {str(e)}")

    else:
        raise HTTPException(status_code=400, detail="Supported formats: .geojson, .zip (shapefile)")

@router.get("/uploads", response_model=list[FileUploadOut])
def list_uploads(db: Session = Depends(get_db)):
    return get_all_uploads(db)

@router.get("/geojson/{upload_id}")
async def get_geojson_by_id(upload_id: int, db: Session = Depends(get_db)):
    uploads = get_all_uploads(db)
    selected = next((u for u in uploads if u.id == upload_id and u.filename.endswith(".geojson")), None)

    if not selected:
        raise HTTPException(status_code=404, detail="GeoJSON upload not found")

    upload_folder = "uploads"
    path = os.path.join(upload_folder, selected.filename)

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found on disk")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
