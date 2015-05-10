from django.shortcuts import render

def home(request):
    """A view of all data."""
    return render(request, 'index.html', {'data': []})
