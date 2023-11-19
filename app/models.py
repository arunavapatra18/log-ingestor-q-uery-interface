from pydantic import BaseModel, ValidationError
from typing import Optional
from datetime import datetime

class Metadata(BaseModel):
    """
    Model of the nested metadata field. 
    Optional field.
    """
    
    parentResourceId: Optional[str]

    
class LogItem(BaseModel):
    """
    Model of the logs
    Inherits the BaseModel class from Pydantic
    """
    
    level: str
    message: str
    resourceId: str
    timestamp: datetime
    traceId: str
    spanId: str
    commit: str
    metadata: Optional[Metadata]
    
def validate_postgres_log_item(log_item: LogItem):
    """
    Validate the pydantic log model

    Args:
        log_item (LogItem): The pydantic log model to validate

    Raises:
        ValidationError: Field type mismatch
        ValidationError: metadata mismatch
    """
    expected_types = {
        'level': str,
        'message': str, 
        'resourceId': str,
        'timestamp': datetime,
        'traceId': str, 
        'spanId': str,
        'commit': str
    }
    
    # Check for type mismatch in the received model
    for field, expected_type in expected_types.items():
        if not isinstance(getattr(log_item, field), expected_type):
            raise ValidationError(
                f'{field} must be of type {expected_type.__name__}'
            )
    
    # Check if metadata field contains Metadata , otherwise None        
    if not isinstance(log_item.metadata, Metadata) and log_item.metadata is not None:
        raise ValidationError(
            'metadata must be of type Metadata or None'
        )