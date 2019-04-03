from django.db import models
from django.utils.timezone import now


class Document(models.Model):
    todo_id = models.AutoField(primary_key=True)
    userid=models.CharField(max_length=255, blank=True,default="anudeep")
    task = models.CharField(max_length=255, blank=True)
    date = models.DateField()
    time = models.TimeField()
    status=models.CharField(max_length=255, blank=True,default="incomplete")

    def __unicode__(self):
        return self.todo_id

