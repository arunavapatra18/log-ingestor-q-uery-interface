from tortoise import fields
from tortoise.models import Model
    
class PostgresLogModel(Model):
    """
    Tortoise ORM Model for Logs
    """
    id = fields.UUIDField(pk=True)
    level = fields.CharField(max_length=255)
    message = fields.TextField()
    resourceId = fields.CharField(max_length=255)
    timestamp = fields.DateField()
    traceId = fields.CharField(max_length=255)
    spanId = fields.CharField(max_length=255)
    commit = fields.CharField(max_length=255)
    metadata = fields.JSONField(null = True)
    
    class Meta:
        table = "postgres_logs"
