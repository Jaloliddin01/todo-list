from django.http import HttpRequest, JsonResponse
from .models import Task
import json
from django.core.exceptions import ObjectDoesNotExist
from django.views import View

def to_dict(task):
    data = {
        'id': task.id,
        'name': task.name,
        'completed': task.completed,
        'desciption': task.description,
        'created': task.created,
        'updated': task.updated,
        'user' : task.user.username, 
    }

    return data

class Tasks(View):

    def get(self, request: HttpRequest, id = None) -> JsonResponse:
        '''get all tasks'''
        if id == None:
            tasks = Task.objects.all()
            data = {'tasks': []}

            for task in tasks:
                data['tasks'].append(to_dict(task))
            return JsonResponse(data)
        else:
            try:
                task = Task.objects.get(pk=id)
                return JsonResponse(to_dict(task))
            except ObjectDoesNotExist:
                return JsonResponse({"status": "does not exist"})

    def delete(self, request: HttpRequest, id: int) -> JsonResponse:
        task = Task.objects.get(pk=id)
        task.delete()
        return JsonResponse({})
    
    def post(self, request: HttpRequest, id: int) -> JsonResponse:
        data = json.loads(request.body.decode("utf-8"))
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

class Tasks_id(View):
    def get(self, request: HttpRequest, id: int) -> JsonResponse:
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

class Tasks_create(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        data = json.loads(request.body.decode("utf-8"))
        task = Task.objects.create(
            name=data['name'],
            description=data['description'],
            completed=data['completed'],
        )
        data = {'task': 
            {
                'id': task.id,
                'name': task.name,
                'completed': task.completed,
                'desciption': task.description,
                'created': task.created,
                'updated': task.updated,
            }
        }
        return JsonResponse(data)

class Complete(View):
    def get(self, request: HttpRequest, id: int) -> JsonResponse:
        if id is not None:
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

class Completed(View):
    def get(self, request: HttpRequest) -> JsonResponse:
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

class Uncompleted(View):
    def get(self, request: HttpRequest) -> JsonResponse:
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
