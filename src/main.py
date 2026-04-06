import sys
from pathlib import Path

from fastapi import APIRouter, FastAPI
import uvicorn 

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities
from src.api.images import router as router_images
from src.listeners import lifespan


app = FastAPI(lifespan=lifespan)

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(router_auth)
api_router.include_router(router_hotels)
api_router.include_router(router_rooms)
api_router.include_router(router_bookings)
api_router.include_router(router_facilities)
api_router.include_router(router_images)

app.include_router(api_router)
    

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)