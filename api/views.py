from django.http import HttpRequest, JsonResponse
from .models import Task

def get_all(request: HttpRequest) -> JsonResponse:
    '''get all tasks'''
    tasks = Task.objects.all()
    data = {'tasks': []}

    for task in tasks:
        data['tasks'].append({
            'id': task.id,
            'name': task.name,
            'completed': task.completed,
            'desciption': task.description,
            'created': task.created,
            'updated': task.updated,
        })

    return JsonResponse(data)

def get_by_id(request: HttpRequest, id: int) -> JsonResponse:
    task = Task.objects.get(pk=id)
    data = {'task': {
        'id': task.id,
        'name': task.name,
        'completed': task.completed,
        'desciption': task.description,
        'created': task.created,
        'updated': task.updated,
    }}
    return JsonResponse(data)

def create(request: HttpRequest) -> JsonResponse:
    data = request.POST
    task = Task.objects.create(
        name=data['name'],
        description=data['description'],
        completed=data['completed'],
    )
    data = {'task': {
        'id': task.id,
        'name': task.name,
        'completed': task.completed,
        'desciption': task.description,
        'created': task.created,
        'updated': task.updated,
    }}
    return JsonResponse(data)

def upadate_by_id(request: HttpRequest, id: int) -> JsonResponse:
    data = request.POST
    task = Task.objects.get(pk=id)
    task.name = data['name']
    task.description = data['description']
    task.completed = data['completed']
    task.save()
    data = {'task': {
        'id': task.id,
        'name': task.name,
        'completed': task.completed,
        'desciption': task.description,
        'created': task.created,
        'updated': task.updated,
    }}
    return JsonResponse(data)

def complete_by_id(request: HttpRequest, id: int) -> JsonResponse:
    task = Task.objects.get(pk=id)
    task.completed = True
    task.save()
    data = {'task': {
        'id': task.id,
        'name': task.name,
        'completed': task.completed,
        'desciption': task.description,
        'created': task.created,
        'updated': task.updated,
    }}
    return JsonResponse(data)

def delete_by_id(request: HttpRequest, id: int) -> JsonResponse:
    task = Task.objects.get(pk=id)
    task.delete()
    data = {'task': {
        'id': task.id,
        'name': task.name,
        'completed': task.completed,
        'desciption': task.description,
        'created': task.created,
        'updated': task.updated,
    }}
    return JsonResponse(data)

def get_all_completed(request: HttpRequest) -> JsonResponse:
    tasks = Task.objects.filter(completed=True)
    data = {'tasks': []}

    for task in tasks:
        data['tasks'].append({
            'id': task.id,
            'name': task.name,
            'completed': task.completed,
            'desciption': task.description,
            'created': task.created,
            'updated': task.updated,
        })

    return JsonResponse(data)

def get_all_uncompleted(request: HttpRequest) -> JsonResponse:
    tasks = Task.objects.filter(completed=False)
    data = {'tasks': []}

    for task in tasks:
        data['tasks'].append({
            'id': task.id,
            'name': task.name,
            'completed': task.completed,
            'desciption': task.description,
            'created': task.created,
            'updated': task.updated,
        })

    return JsonResponse(data)
