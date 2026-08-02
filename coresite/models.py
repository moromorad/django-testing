# pyrefly: ignore [missing-import]
from django.db import models
# pyrefly: ignore [missing-import]
from django.db.models.signals import post_delete
# pyrefly: ignore [missing-import]
from django.dispatch import receiver


# Create your models here.
class Task(models.Model):
    # The actual text of the to-do item
    title = models.CharField(max_length=200, unique=True)
    
    # Is it done? Defaults to False when created.
    completed = models.BooleanField(default=False)
    
    # Automatically saves the exact timestamp when a task is first created
    created_at = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(
    "auth.User", related_name="tasks", on_delete=models.CASCADE
    )

    
    def __str__(self):
        # This just makes the task readable in the console (returns "Buy Milk" instead of "Task Object 1")
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
