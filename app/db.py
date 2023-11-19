from os import getenv
from dotenv import load_dotenv
from tortoise import Tortoise
from pymongo import MongoClient

from .storage import PostgresLogModel

# Load env variables
load_dotenv()

# DB URLS : Please update with your Postgres and MongoDB urls. Also update the .env with the correct credentials.
POSTGRES_DB_URL = f"postgres://{getenv('DB_USERNAME')}:{getenv('DB_PASSWORD')}@localhost:5432/{getenv('DB_NAME')}"
MONGO_DB_URL = f"mongodb+srv://{getenv('MONGO_DB_USERNAME')}:{getenv('MONGO_DB_PASSWORD')}@cluster0.u2ntfqh.mongodb.net/?retryWrites=true&w=majority"

# Postgres DB Setup
async def pg_db_init():
    """
    Initialize postgres db
    """
    
    print("Connecting to Postgres DB")
    await Tortoise.init(
        db_url=POSTGRES_DB_URL,
        modules={
            'models': ['app.storage']
        }
    )
    print("Generating schema")
    await Tortoise.generate_schemas()
    print("Connection Established")
    
async def close():
    """
    Close postgres db connection
    """
    await Tortoise.close_connections()
    print("Connection Closed")
    
async def save_log(log_item: PostgresLogModel):
    """
    Save the Tortoise ORM log model to DB

    Args:
        log_item (PostgresLogModel): Tortoise ORM model of the log data
    """
    await log_item.save()
    
# MongoDB Setup

client = MongoClient(MONGO_DB_URL)
mongo_logs_db = client.get_database("mongo-logs")
logs_collection = mongo_logs_db.get_collection("logs_collection")

# Indexing fields for search
index_fields = [
    ("level", "text"),
    ("message", "text"),
    ("resourceId", "text"),
    ("timestamp", "text"),
    ("traceId", "text"),
    ("spanId", "text"),
    ("commit", "text"),
    ("metadata.parentResourceId", "text")
]

logs_collection.create_index(index_fields)
