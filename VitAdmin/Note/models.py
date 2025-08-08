from django.db import models

class User(models.Model):
    us_id = models.CharField(primary_key=True, max_length=20)
    us_name = models.CharField(max_length=100)
    us_email = models.CharField(max_length=100)
    us_password = models.CharField(max_length=100)
    us_img = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.us_name

class Note(models.Model):
    nt_id = models.CharField(primary_key=True, max_length=20)
    nt_title = models.CharField(max_length=100)
    nt_subtitle = models.CharField(max_length=100, blank=True, null=True)
    nt_content = models.TextField(blank=True, null=True)
    nt_img = models.CharField(max_length=255, blank=True, null=True)
    nt_pdf = models.CharField(max_length=255, blank=True, null=True)
    nt_date = models.DateTimeField()
    us = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nt_title