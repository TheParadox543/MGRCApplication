from fastapi import FastAPI
import uvicorn
from app.api.routes import office_user_routes, admin_routes
from app.database import ping_server

# from app.database import connect_to_mongo
# from app.api.routes import office_user_routes, admin_routes

app = FastAPI()

app.include_router(office_user_routes.router)
app.include_router(admin_routes.router)


@app.get("/")
def read_root():
    return {"message": "MGRC Backend is running 🎉"}


@app.get("/pingdb")
async def ping_db():
    await ping_server()
    return {
        "message": "Pinged your deployment from route. You successfully connected to MongoDB!"
    }
