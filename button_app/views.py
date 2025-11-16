from django.shortcuts import render
from .models import ClickCounter

def index(request):
    counter = ClickCounter.get_singleton()
    context = {
        'initial_count': counter.count
    }
    return render(request, 'button_app/index.html', context)