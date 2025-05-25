from fastapi import FastAPI, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# DB and model imports
from backend.db.database import Base, engine
from backend.models.asset_model import Asset
from backend.routers import assets

app = FastAPI()

# Enable CORS (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with allowed origins in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event: connect to DB and create tables
@app.on_event("startup")
def startup_event():
    try:
        Base.metadata.create_all(bind=engine)  # Auto-create tables
        engine.connect()
        print("✅ Database connected successfully and tables are ready.")
        print(f"📦 Using DB: {engine.url}")  # Shows SQLite path
    except Exception as e:
        print("❌ Failed to connect to the database:", e)

# Root route
#@app.get("/")
#def read_root():
#    return {"message": "Welcome to the GIS Developer App"}

# 404 Not Found Handler
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": "The requested resource was not found."}
    )

# 500 Internal Server Error Handler
@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "An internal server error occurred"}
    )
app.include_router(assets.router)

from backend.routers import files
app.include_router(files.router)

# ✅ Serve the static Leaflet map from / (homepage)
from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory="backend/static", html=True), name="static")
