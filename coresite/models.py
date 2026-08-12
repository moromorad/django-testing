# pyrefly: ignore [missing-import]
from django.db import models
# pyrefly: ignore [missing-import]
from django.db.models.signals import post_delete
# pyrefly: ignore [missing-import]
from django.dispatch import receiver


from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100)
    github_repo = models.CharField(
        max_length=200, help_text="e.g. 'owner/repository'"
    )
    ast_outline = models.TextField(blank=True, default="")
    owner = models.ForeignKey(
        "auth.User", related_name="projects", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    class TicketType(models.TextChoices):
        BUG = "bug", "Bug"
        FEATURE = "feature", "Feature"
        CHORE = "chore", "Chore"

    title = models.CharField(max_length=200)

    # Is it done? Defaults to False when created.
    completed = models.BooleanField(default=False)

    # Automatically saves the exact timestamp when a task is first created
    created_at = models.DateTimeField(auto_now_add=True)

    due_date = models.DateTimeField(null=True, blank=True)

    owner = models.ForeignKey(
        "auth.User", related_name="tasks", on_delete=models.CASCADE
    )

    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,
        blank=True,
    )
    ticket_type = models.CharField(
        max_length=10,
        choices=TicketType.choices,
        default=TicketType.FEATURE,
    )
    # Stores subtasks as a list of dicts, e.g. [{"title": "Check auth middleware", "done": False}]
    subtasks = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.title   
    
class Weather(models.Model):
    temp = models.FloatField()
    time = models.DateTimeField()
    weather = models.CharField(max_length=200)
    weather_code = models.IntegerField(default=0)
    class Meta:
        ordering = ['-time'] 
    def __str__(self):
        return f"{self.weather} ({self.temp}°C) at {self.time.strftime('%Y-%m-%d %H:%M')}"
    

# 1. We use the @receiver decorator to tell Django to listen for 'post_delete' on the 'Task' model
@receiver(post_delete, sender=Task)
def notify_task_deleted(sender, instance, **kwargs):
    # 2. 'instance' is the actual task object that was just deleted
    print("\n-------------------------------------------------------------")
    print(f"💥 SIGNAL ALARM: The task '{instance.title}' was just deleted!")
    print("-------------------------------------------------------------\n")
