from django.db import models

# Create your models here.
class UserInputHistory(models.Model):
    """
    Lưu tất cả câu hỏi từ user và kết quả trả về lần đầu của AI.
    """
    user_input = models.TextField()
    intent = models.CharField(max_length=50, blank=True, null=True)
    ai_output = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.id}] {self.intent} - {self.user_input[:30]}"


class AIFeedback(models.Model):
    """
    Lưu phản hồi từ user và kết quả AI sửa lại.
    """
    history = models.ForeignKey(UserInputHistory, on_delete=models.CASCADE, related_name="feedbacks")
    feedback_text = models.TextField()  # Ghi chú sửa lỗi từ user
    ai_correction = models.TextField(blank=True, null=True)  # Kết quả AI sau khi sửa
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.id}] Feedback for History {self.history.id}"