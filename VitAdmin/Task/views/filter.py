from django.http import JsonResponse
from django.db.models import Q
from Common.models import Task

def filter_tasks(request):
    title = request.GET.get("title")
    start_from = request.GET.get("start_from")
    start_to = request.GET.get("start_to")
    note = request.GET.get("note")
    ws_id = request.GET.get("ws_id")

    filters = Q()

    if title:
        filters &= Q(ts_title__icontains=title)

    if start_from and start_to:
        filters &= Q(ts_start__range=[start_from, start_to])
    elif start_from:
        filters &= Q(ts_start__gte=start_from)
    elif start_to:
        filters &= Q(ts_start__lte=start_to)

    if note:
        filters &= Q(ts_note__icontains=note.strip())  # tìm theo cụm từ, không phân biệt hoa thường

    if ws_id:
        filters &= Q(ws__ws_id=ws_id)

    tasks = Task.objects.filter(filters).select_related("ws", "us")

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
            "user": t.us.us_name,
        }
        for t in tasks
    ]

    return JsonResponse({"tasks": data})
