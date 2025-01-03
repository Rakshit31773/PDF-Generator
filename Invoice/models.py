import uuid
from django.db import models
from datetime import datetime
from zoneinfo import ZoneInfo

def get_current_time_utc530():
    tz = ZoneInfo("Asia/Kolkata")  # UTC+05:30 timezone
    return datetime.now(tz)

ADDRESS_CATEGORY = (
    ('Gujarat Refinery','Gujarat Refinery'),
)

RETURNABLE_CATEGORY = (
    ('Returnable','Returnable'),
    ('Non-Returnable','Non-Returnable'),
)

NAMES = (
    ('Kesaba Trilochan Panda','Kesaba Trilochan Panda'),
    ('Rakshit Singh','Rakshit Singh'),
)

# Create your models here.
class letter_information(models.Model):
    letter_id = models.UUIDField(default=uuid.uuid4, unique=True)
    address = models.CharField(max_length=30, choices=ADDRESS_CATEGORY)
    returnable = models.CharField(max_length=20, choices=RETURNABLE_CATEGORY)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    date = models.DateTimeField(default=get_current_time_utc530)
    name=models.CharField(max_length=50, choices=NAMES)

    def __str__(self):
        # return f'{self.returnable} pass from {self.address} to {self.destination}'
        return f'{self.letter_id}'
    
    
class list_of_items(models.Model):
    table_id = models.CharField(max_length=150)
    description = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural='list_of_items'
    
