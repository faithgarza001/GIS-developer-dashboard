
# Import the FastAPI framework, which is used to create web APIs
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import status

#create an instance of the FastAPI class
app = FastAPI()

#add Cors
app.add_middleware(
       CORSMiddleware,
    allow_origins=["*"],  # Replace * with a list of allowed origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)


#define a route for the route URL("/")
@app.get("/")
def read_root():
    #This function will be called when a GET Request is made to the root of the URL
    #It returns a JSON response with a welcome message
    return {"message": "Welcome to the GIS Developer App"}
#404 Not Found Handler
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


