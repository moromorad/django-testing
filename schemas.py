from pydantic import BaseModel, ConfigDict
from datetime import datetime

# 3.5. Pydantic Models
class TaskCreate(BaseModel):
    title: str
    completed: bool = False  # Default to False if the user doesn't send it

class TaskResponse(BaseModel):
    title: str
    completed: bool
    created_at: datetime
    
    # This magic line allows Pydantic to read Django ORM objects
    model_config = ConfigDict(from_attributes=True)
