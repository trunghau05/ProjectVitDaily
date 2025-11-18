from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Common.models import Task, User

@api_view(['POST'])
def AddTask(request):
    try:
        # Lấy dữ liệu từ request
        title = request.data.get('ts_title')
        subtitle = request.data.get('ts_subtitle', '')
        note = request.data.get('ts_note', '')
        status_task = request.data.get('ts_status', 0)
        start_date = request.data.get('ts_start')
        end_date = request.data.get('ts_end')
        us_id = request.data.get('us_id')

        # Kiểm tra thông tin bắt buộc
        if not all([title, start_date, end_date, us_id]):
            return Response(
                {"error": "Thiếu thông tin bắt buộc (ts_title, ts_start, ts_end, us_id)."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Kiểm tra user có tồn tại không
        try:
            user = User.objects.get(pk=us_id)
        except User.DoesNotExist:
            return Response({"error": "User không tồn tại"}, status=status.HTTP_404_NOT_FOUND)

        # Kiểm tra logic ngày tháng
        if end_date < start_date:
            return Response({"error": "Ngày kết thúc phải sau ngày bắt đầu"}, status=status.HTTP_400_BAD_REQUEST)

        # Tạo mã task tự động (VD: TS001)
        total_tasks = Task.objects.count()
        new_id = f"TS{str(total_tasks + 1).zfill(3)}"

        # Tạo task mới
        task = Task.objects.create(
            ts_id=new_id,
            ts_title=title,
            ts_subtitle=subtitle,
            ts_note=note,
            ts_status=int(status_task),
            ts_start=start_date,
            ts_end=end_date,
            us=user
        )

        # Trả về kết quả
        return Response({
            "message": "Tạo task thành công",
            "task_id": task.ts_id
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
