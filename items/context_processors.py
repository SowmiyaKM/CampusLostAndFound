from .models import Notification


def notifications_processor(request):
    if request.user.is_authenticated:
        qs = Notification.objects.filter(user=request.user)
        return {
            'nav_notifications': qs[:6],
            'nav_unread_count': qs.filter(is_read=False).count(),
        }
    return {'nav_notifications': [], 'nav_unread_count': 0}
