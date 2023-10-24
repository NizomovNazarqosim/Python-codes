from django.shortcuts import render
from .models import Team

def index(request):
    teams = Team.objects.all()
    return render(request, 'index.html', {'teams': teams})


def attendance_detail(request, team_id):
    team = Team.objects.get(id=team_id)
    return render(request, 'detail.html', {'team':team})