from django.http import JsonResponse
from Common.models import Task
from ..models import Task
def TaskList(request):
    us_id = request.GET.get("us_id")  
    if not us_id:
        return JsonResponse({"error": "Missing us_id"}, status=400)

    tasks = Task.objects.filter(us__us_id=us_id).select_related('ws')
    data = [
        {
            "ts_id": t.ts_id,
            "ts_title": t.ts_title,
            "ts_subtitle": t.ts_subtitle,
            "ts_status": t.ts_status,
            "ts_start": t.ts_start,
            "ts_end": t.ts_end,
            "ts_note": t.ts_note,
            "us_id": t.us.us_id, 
            "ws_id": t.ws.ws_id if t.ws else None,
        }
        for t in tasks
    ]
    return JsonResponse(data, safe=False)