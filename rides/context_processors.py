from .models import RideRequest

def pending_requests_count(request):
    if request.user.is_authenticated and request.user.Driver_Status:
        count = RideRequest.objects.filter(
            ride__driver=request.user,
            status='pending'
        ).count()
        return {'pending_requests_count': count}
    return {'pending_requests_count': 0}