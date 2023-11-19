from .api import LogIngestorAPI
from .db import pg_db_init, close

def create_app():
    """
    Initializes LogIngestorAPI instance and gets the FastAPI instance.
    Handles database postgres db init and close.

    Returns:
        app: FastAPI() instance
    """
    log_ingestor = LogIngestorAPI()
    app = log_ingestor.app
    
    async def startup_event():
        """
        Startup Event for the App
        Initialize the postgres database
        """
        await pg_db_init()
    
    async def shutdown_event():
        """
        Shutdown Event for the App
        Close the database connection
        """
        await close()
        
    app.add_event_handler("startup", startup_event)
    app.add_event_handler("shutdown", shutdown_event)
    
    return app
