from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List, Optional

# 3.5. Pydantic Models
class TaskCreate(BaseModel):
    title: str = Field(description="The title or description of the task to be created")
    completed: bool = Field(default=False, description="Whether the task is already completed (defaults to False)")
    due_date: Optional[datetime] = Field(default=None, description="The date and time when the task is due, if applicable, in ISO 8601 format with timezone offset (e.g., YYYY-MM-DDTHH:MM:SS+03:00)")


class TaskCreateList(BaseModel):
    tasks: List[TaskCreate] = Field(description="A list of tasks to create")


class TaskResponse(BaseModel):
    title: str = Field(description="The title or description of the task")
    completed: bool = Field(description="Whether the task is completed")
    created_at: datetime = Field(description="The timestamp when the task was created")
    due_date: Optional[datetime] = Field(default=None, description="The date and time when the task is due, if applicable, in ISO 8601 format with timezone offset (e.g., YYYY-MM-DDTHH:MM:SS+03:00)")
    
    # This magic line allows Pydantic to read Django ORM objects
    model_config = ConfigDict(from_attributes=True)
