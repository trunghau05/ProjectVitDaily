from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .trains import run_ai 

@csrf_exempt
def ai_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            us_input = data.get("us_input")
            us_id = data.get("us_id")  # Lấy us_id từ POST
            if not us_input:
                return JsonResponse({"error": "us_input is required"}, status=400)
            if not us_id:
                return JsonResponse({"error": "us_id is required"}, status=400)

            result, intent = run_ai(us_input, us_id=us_id)  # Truyền us_id vào run_ai
            return JsonResponse({"intent": intent, "result": result})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)
