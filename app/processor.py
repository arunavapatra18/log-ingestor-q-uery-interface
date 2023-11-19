from .models import LogItem, validate_postgres_log_item
from .storage import PostgresLogModel
from .db import logs_collection

class PostgresLogProcessor:
    
    async def process_log(self, log_item: LogItem):
        """
        Validate the pydantic log model and create a PostgresLogModel from the pydantic model.

        Args:
            log_item (LogItem): Pydantic log model

        Returns:
            PostgresLogModel: The tortoise ORM model created from pydantic model
        """
        validate_postgres_log_item(log_item)
        structured_log = await PostgresLogModel.create(**log_item.model_dump())
        return structured_log
        
class MongoLogProcessor:
    
    def process_log(self, log_item: LogItem):
        """
        Insert the pydantic log into mongo db collections

        Args:
            log_item (LogItem): Pydantic log model
        """
        logs_collection.insert_one(log_item.model_dump())   
