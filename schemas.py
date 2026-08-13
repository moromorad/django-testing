from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional



# 3.5. Pydantic Models


class TaskCreate(BaseModel):
    title: str = Field(description="A short, descriptive title for the ticket")
    description: str = Field(default="", description="MUST NOT BE EMPTY. Detailed technical instructions on how to implement the task, referencing specific files and functions from the AST.")
    ticket_type: Literal["bug", "feature", "chore"] = Field(default="feature", description="The type of ticket: bug, feature, or chore")
    due_date: Optional[datetime] = Field(default=None, description="The date and time when the task is due in ISO 8601 format with timezone offset. Leave null if no deadline.")
    completed: bool = Field(default=False, description="Whether the task is already completed")
    subtasks: List[SubTask] = Field(default_factory=list, description="MUST NOT BE EMPTY. A list of technical subtasks required to complete this ticket")

class SubTask(BaseModel):
    title: str = Field(description="The title of the subtask")
    completed: bool = Field(default=False, description="Whether the subtask is completed")

class TaskCreateList(BaseModel):
    tasks: List[TaskCreate] = Field(description="A list of tasks to create")


class TaskResponse(BaseModel):
    title: str = Field(description="The title or description of the task")
    completed: bool = Field(description="Whether the task is completed")
    created_at: datetime = Field(description="The timestamp when the task was created")
    due_date: Optional[datetime] = Field(default=None, description="The date and time when the task is due, if applicable, in ISO 8601 format with timezone offset (e.g., YYYY-MM-DDTHH:MM:SS+03:00)")
    
    # This magic line allows Pydantic to read Django ORM objects
    model_config = ConfigDict(from_attributes=True)
