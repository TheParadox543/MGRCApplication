from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import asyncio
from pymongo.server_api import ServerApi
from app.models.office_user_model import OfficeUserDB, OfficeUserCreate, OfficeUserBase

# Load environment variables from .env file
load_dotenv()

# Read the Mongo URI from .env
MONGO_URI = os.getenv("MONGO_URI_LOCAL")

client = AsyncIOMotorClient(MONGO_URI, server_api=ServerApi("1"))
db = client["MGRC_DB"]
office_user_collection = db["office_users"]
life_members_collection = db["life_members"]


async def ping_server():
    # Set the Stable API version when creating a new client
    # client = AsyncIOMotorClient(MONGO_URI, server_api=ServerApi("1"))
    # Send a ping to confirm a successful connection
    try:
        await client.admin.command("ping")
        print(
            "Pinged your deployment from function. You successfully connected to MongoDB!"
        )
    except Exception as e:
        print(e)


async def find_office_user_by_username(user_name: str):
    user = await office_user_collection.find_one({"_id": user_name})
    if user:
        user["id"] = user.pop("_id")
        user_object = OfficeUserBase(**user)
        return user_object
    else:
        return None

async def insert_user(new_user: OfficeUserDB):
    # Check if the user already exists
    existing_user = await find_office_user_by_username(new_user.id)
    if existing_user:
        print("User already exists")
        return

    # Insert the new user into the database
    result = await office_user_collection.insert_one(new_user.model_dump())
    print(f"User inserted with id: {result.inserted_id}")
    return result


if __name__ == "__main__":
    loop = client.get_io_loop()
    loop.run_until_complete(ping_server())

# asyncio.run(insert_user())
