from django.utils.deprecation import MiddlewareMixin
from Common.models import User

class SessionUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_id = request.session.get("user_id")
        if user_id:
            try:
                request.user_session = User.objects.get(us_id=user_id)
            except User.DoesNotExist:
                request.user_session = None
        else:
            request.user_session = None
    