from django.db import models

class User(models.Model):
    us_id = models.CharField(primary_key=True, max_length=20)
    us_name = models.CharField(max_length=100)
    us_email = models.CharField(max_length=100)
    us_password = models.CharField(max_length=100)
    us_img = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.us_name
    
class WorkSpace(models.Model):
    ws_id = models.CharField(primary_key=True, max_length=20)
    ws_name = models.CharField(max_length=100)
    us = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.ws_name

class InSpace(models.Model):
    is_id = models.CharField(primary_key=True, max_length=20)
    is_role = models.CharField(max_length=50)
    ws = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    us = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.us.us_name} in {self.ws.ws_name} - {self.is_role}"
    
class Task(models.Model):
    ts_id = models.CharField(primary_key=True, max_length=20)
    ts_title = models.CharField(max_length=100)
    ts_subtitle = models.CharField(max_length=100, blank=True, null=True)
    ts_status = models.BooleanField(default=False)
    ts_start = models.DateField()
    ts_end = models.DateField()
    ts_note = models.TextField(blank=True, null=True)
    us = models.ForeignKey(User, on_delete=models.CASCADE)
    ws = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)

    def __str__(self):
        return self.ts_title

class Subtask(models.Model):
    st_id = models.CharField(primary_key=True, max_length=20)
    st_title = models.CharField(max_length=100)
    st_subtitle = models.CharField(max_length=100, blank=True, null=True)
    st_note = models.TextField(blank=True, null=True)
    st_status = models.BooleanField(default=False)
    st_start = models.DateField()
    st_end = models.DateField()
    us = models.ForeignKey(User, on_delete=models.CASCADE)
    ts = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return self.st_title
    
class Todo(models.Model):
    td_id = models.CharField(primary_key=True, max_length=20)
    td_type = models.CharField(max_length=100)
    td_status = models.BooleanField(default=False)
    st = models.ForeignKey(Subtask, on_delete=models.CASCADE, blank=True, null=True)
    ts = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.td_type

class UsedTask(models.Model):
    ut_id = models.CharField(primary_key=True, max_length=20)
    us = models.ForeignKey(User, on_delete=models.CASCADE)
    ts = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.us.us_name} - {self.ts.ts_title}"