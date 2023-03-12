import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from myapp.utils.client import *

def index(request):
    return render(request, 'index.html')

def loadNotes(request):
    notes = getAllNotes()
    return JsonResponse(notes, safe=False)

@csrf_exempt
def saveNote(request):
    if request.method == 'POST':
        topic = request.POST.get('topic')
        title = request.POST.get('title')
        text = request.POST.get('text')
        saveNewNote(topic, title, text)
        return HttpResponse('OK')
    else:
        return HttpResponse('Only POST allowed')
