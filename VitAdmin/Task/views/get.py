# views.py
from django.http import JsonResponse
from models import Task

def get_tasks(request):
    us_id = request.GET.get("us_id")  # nhận từ query string
    if not us_id:
        return JsonResponse({"error": "Missing us_id"}, status=400)

    tasks = Task.objects.filter(us__us_id=us_id).select_related('ws')
    data = [
        {
            "id": t.ts_id,
            "title": t.ts_title,
            "subtitle": t.ts_subtitle,
            "status": t.ts_status,
            "start": t.ts_start,
            "end": t.ts_end,
            "note": t.ts_note,
            "workspace": t.ws.ws_name,
        }
        for t in tasks
    ]
    return JsonResponse({"tasks": data})
