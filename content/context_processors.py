from .models import Thinker

def get_thinkers(request):
    thinkers = Thinker.objects.all().order_by("name")
    return {"thinkers":thinkers}