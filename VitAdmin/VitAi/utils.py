from django.db import transaction
from Common.models import User, Feedback, History

def save_feedback(user_input, intent, ai_output, us_id="US001"):
    if intent != "feedback":
        return None

    try:
        user = User.objects.get(us_id=us_id)
    except User.DoesNotExist:
        raise ValueError(f"User {us_id} không tồn tại")

    with transaction.atomic():
        last_feedback = Feedback.objects.order_by('-fb_id').first()
        if last_feedback and last_feedback.fb_id.startswith("FB"):
            last_number = int(last_feedback.fb_id[2:])
            new_number = last_number + 1
        else:
            new_number = 1

        new_fb_id = f"FB{new_number:03d}"
        feedback_text = f"User Input: {user_input}\nAI Output: {ai_output}"

        feedback = Feedback.objects.create(
            fb_id=new_fb_id,
            intent=intent,
            feedback_text=feedback_text,
            us=user
        )

    return feedback


def get_feedback_user_inputs(us_id="US001"):
    try:
        user = User.objects.get(us_id=us_id)
    except User.DoesNotExist:
        raise ValueError(f"User {us_id} không tồn tại")

    qs = Feedback.objects.filter(intent="feedback", us=user)
    feedback_texts = qs.values_list('feedback_text', flat=True)
    return list(feedback_texts)


def save_history(user_input, intent, ai_output, us_id="US001"):
    try:
        user = User.objects.get(us_id=us_id)
    except User.DoesNotExist:
        raise ValueError(f"User {us_id} không tồn tại")

    history = History.objects.create(
        user_input=user_input,
        intent=intent,
        ai_output=ai_output,
        us=user
    )
    return history


def get_last_user_input(us_id="US001", max_n=50):
    try:
        user = User.objects.get(us_id=us_id)
    except User.DoesNotExist:
        raise ValueError(f"User {us_id} không tồn tại")

    qs = History.objects.filter(us=user).order_by('-created_at')
    
    last_inputs = list(qs[:max_n])

    if qs.count() > max_n:
        keep_ids = [h.id for h in last_inputs]  
        History.objects.filter(us=user).exclude(id__in=keep_ids).delete()

    if not last_inputs:
        return ""
    
    history_text = "\n".join(
        f"User: {h.user_input}\nVitAi: {h.ai_output}"
        for h in reversed(last_inputs)
    )
    
    print(history_text)
    return history_text
