from django.db import models
from django.utils import timezone
from datetime import timedelta

# ===============================
# Bảng User
# ===============================
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    us_id = models.CharField(max_length=10, primary_key=True)
    us_name = models.CharField(max_length=100)
    us_email = models.EmailField(unique=True)
    us_password = models.CharField(max_length=128)
    us_img = models.CharField(max_length=255, blank=True, null=True)
    failed_attempts = models.IntegerField(default=0)
    lock_until = models.DateTimeField(blank=True, null=True)
    @property
    def id(self):
        return self.us_id  # trả về us_id khi SimpleJWT gọi user.id

    def set_password(self, raw_password):
        self.us_password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.us_password)

    def register_failed_attempt(self):
        self.failed_attempts += 1
        if self.failed_attempts >= 3:
            self.lock_until = timezone.now() + timedelta(minutes=5)
        self.save()

    def reset_lock(self):
        self.failed_attempts = 0
        self.lock_until = None
        self.save()

    def is_locked(self):
        if self.lock_until and timezone.now() < self.lock_until:
            return True
        return False


class Verification(models.Model):
    us = models.ForeignKey(User, on_delete=models.CASCADE)
    vc_otp = models.CharField(max_length=6)
    vc_status = models.BooleanField(default=False)
    vc_start = models.DateTimeField(auto_now_add=True)
    vc_end = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.vc_end:
            self.vc_end = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)



# ===============================
# Bảng WorkSpace
# ===============================
class WorkSpace(models.Model):
    ws_id = models.CharField(primary_key=True, max_length=20)
    ws_name = models.CharField(max_length=100)
    us = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.ws_name


# ===============================
# Bảng InSpace
# ===============================
class InSpace(models.Model):
    is_id = models.CharField(primary_key=True, max_length=20)
    is_role = models.CharField(max_length=50)
    ws = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    us = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.us.us_name} in {self.ws.ws_name} - {self.is_role}"


# ===============================
# Bảng Note
# ===============================
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


# ===============================
# Bảng Task
# ===============================
class Task(models.Model):
    ts_id = models.CharField(primary_key=True, max_length=20)
    ts_title = models.CharField(max_length=100)
    ts_subtitle = models.CharField(max_length=100, blank=True, null=True)
    ts_status = models.IntegerField(default=False)
    ts_start = models.DateField()
    ts_end = models.DateField()
    ts_note = models.TextField(blank=True, null=True)
    us = models.ForeignKey(User, on_delete=models.CASCADE)
    ws = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.ts_title


# ===============================
# Bảng Subtask
# ===============================
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


# ===============================
# Bảng Todo
# ===============================
class Todo(models.Model):
    td_id = models.CharField(primary_key=True, max_length=20)
    td_type = models.CharField(max_length=100)
    td_status = models.BooleanField(default=False)
    st = models.ForeignKey(Subtask, on_delete=models.CASCADE, blank=True, null=True)
    ts = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.td_type


# ===============================
# Bảng UsedTask
# ===============================
class UsedTask(models.Model):
    ut_id = models.CharField(primary_key=True, max_length=20)
    us = models.ForeignKey(User, on_delete=models.CASCADE)
    ts = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.us.us_name} - {self.ts.ts_title}"


class History(models.Model):
    ht_id = models.CharField(primary_key=True, max_length=20)
    user_input = models.TextField()
    intent = models.CharField(max_length=50, blank=True, null=True)
    ai_output = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    us = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_input} - {self.ai_output}"


class Feedback(models.Model):
    fb_id = models.CharField(primary_key=True, max_length=20)
    intent = models.CharField(max_length=50, blank=True, null=True)
    feedback_text = models.TextField(blank=True, null=True)
    us = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.feedback_text
