from fastapi import FastAPI, Query
from .db import save_log, logs_collection
from .processor import MongoLogProcessor, PostgresLogProcessor
from .models import LogItem

class LogIngestorAPI:
    
    def __init__(self):
        """
        Initializes FastAPI and PostgresLogProcessor
        """
        self.app = FastAPI()
        self.postgres_log_processor = PostgresLogProcessor()
        self.mongo_log_processor = MongoLogProcessor()
        
        @self.app.post("/")
        async def ingest_log(log_item: LogItem):
            """
            API endpoint to ingest log

            Args:
                log_item (LogItem): The pydantic model to validate and store in DB
                
            Returns:
                JSON: Success Message
            """
            formatted_log = await self.postgres_log_processor.process_log(log_item)
            await save_log(formatted_log)
            self.mongo_log_processor.process_log(log_item)
            return {"message": "Log saved successfully"}
        
        @self.app.get("/search")
        def search_logs(
                query: str = Query(None, description="Full-text Search"),
                level: str = Query(None, description="Filter by log level"),
                message: str = Query(None, description="Filter by log message"),
                resource_id: str = Query(None, description="Filter by resource ID"),
                timestamp: str = Query(None, description="Filter by timestamp"),
                trace_id: str = Query(None, description="Filter by trace ID"),
                span_id: str = Query(None, description="Filter by span ID"),
                commit: str = Query(None, description="Filter by commit"),
                parent_resource_id: str = Query(None, description="Filter by parent resource ID"),
            ):
            """
            API endpoint to search and filter existing logs

            Args:
                query (str, optional): text for Full-text Search
                level (str, optional): level filter
                message (str, optional): message filter
                resource_id (str, optional): resourceId filter
                timestamp (str, optional): timestamp filter
                trace_id (str, optional): traceId filter
                span_id (str, optional): spanId filter 
                commit (str, optional): commit filter
                parent_resource_id (str, optional): metadata.parentResourceId filter

            Returns:
                List of LogItem: Search result logs
            """
            
            mongo_query = {}
            
            if query:
                mongo_query["$text"] = {
                    "$search": query
                }
            if level:
                mongo_query["level"] = level
            if message:
                mongo_query["message"] = message
            if resource_id:
                mongo_query["resourceId"] = resource_id
            if timestamp:
                mongo_query["timestamp"] = timestamp
            if trace_id:
                mongo_query["traceId"] = trace_id
            if span_id:
                mongo_query["spanId"] = span_id
            if commit:
                mongo_query["commit"] = commit
            if parent_resource_id:
                mongo_query["metadata.parentResourceId"] = parent_resource_id
                
            query_results = logs_collection.find(mongo_query)
            
            return [LogItem(**log) for log in query_results]