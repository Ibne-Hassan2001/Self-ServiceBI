from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils.timezone import now

class Record(models.Model):
    
    CREATION_CHOICES = [
        ('M3', 'M3'),
        ('Churnback', 'Churnback'),
        ('Activation_DateBased_GA', 'Activation_DateBased_GA'),
        ('PQS_BTS', 'PQS_BTS'),
        ('Network_BTS_GA', 'Network_BTS_GA'),
        ('Single_Device_Report', 'Single_Device_Report'),
    ]

    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('file_generated', 'File Generated'),
        ('email_sent', 'Email Sent'),
    ]

    id = models.BigAutoField(primary_key=True)
    task_id = models.CharField(max_length=100)
    use_cases = models.CharField(max_length=50, choices=CREATION_CHOICES, default='M3')
    creation_date = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='In Progress')
    # end_time = models.DateTimeField(auto_now_add=True)

    
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)





    def __str__(self):
            return f"Record {self.id} - {self.use_cases} - {self.creation_date}"





