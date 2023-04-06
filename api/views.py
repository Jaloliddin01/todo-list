from django.http import HttpRequest, JsonResponse
from .models import Task
import json
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from base64 import b64decode

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

class Registration(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        data = data = json.loads(request.body.decode("utf-8"))
        User(
            username = data['username'],
            password = data['password'],
        ).save()
        return JsonResponse({"status" : "User created"})


class Tasks(View):

    def get(self, request: HttpRequest) -> JsonResponse:
        '''get all tasks'''
        authorization = request.headers.get('Authorization').split()[1]

        username, password = b64decode(authorization).decode().split(':')
        # username, password = authorization['username'], authorization['password']

        user = authenticate(username=username, password=password)
        # print(username, password)
        # print(user)

        if user != None:
            tasks = Task.objects.filter(user=user)
            data = {'tasks': []}

            for task in tasks:
                data['tasks'].append(to_dict(task))
            return JsonResponse(data)
        return JsonResponse({"status": "Unauthorized"})

    def delete(self, request: HttpRequest, id: int) -> JsonResponse:
        # authorizing user
        authorization = request.headers.get('Authorization').split()[1]
        username, password = b64decode(authorization).decode().split(':')
        user = authenticate(username=username, password=password)

        if user != None:
            task = Task.objects.filter(user=user, pk=id)
            task.delete()
            return JsonResponse({"status": "Item was deleted"})
        return JsonResponse({"status": "Unauthorized"})

    
    def post(self, request: HttpRequest, id: int) -> JsonResponse:
        # authorizing user
        authorization = request.headers.get('Authorization').split()[1]
        username, password = b64decode(authorization).decode().split(':')
        user = authenticate(username=username, password=password)

        if user != None:
            data = json.loads(request.body.decode("utf-8"))
            task = Task.objects.filter(user=user, pk=id)
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
        return JsonResponse({"status": "Unauthorized"})

class Tasks_id(View):
    def get(self, request: HttpRequest, id: int) -> JsonResponse:
        authorization = request.headers.get('Authorization').split()[1]
        username, password = b64decode(authorization).decode().split(':')
        user = authenticate(username=username, password=password)

        if user != None:
            task = Task.objects.get(user=user, pk=id)
            if task != None:
                data = {'task': {
                    'id': task.id,
                    'name': task.name,
                    'completed': task.completed,
                    'desciption': task.description,
                    'created': task.created,
                    'updated': task.updated,
                }}
                return JsonResponse(data)
            else:
                return JsonResponse({'status': 'Not found any tasks'})
        return JsonResponse({"status": "Unauthorized"})

class Tasks_create(View):
    def post(self, request: HttpRequest) -> JsonResponse:

        authorization = request.headers.get('Authorization').split()[1]
        username, password = b64decode(authorization).decode().split(':')
        user = authenticate(username=username, password=password)

        if user != None:
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
        return JsonResponse({"status" : "Unauthorized"})

class Complete(View):
    def get(self, request: HttpRequest, id: int) -> JsonResponse:
        authorization = request.headers.get('Authorization').split()[1]
        username, password = b64decode(authorization).decode().split(':')
        user = authenticate(username=username, password=password)

        if user != None and id is not None:
            task = Task.objects.filter(user=user, pk=id)
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
        if user is None:
            return JsonResponse({"status" : "Unauthorized"})
        else:
            return JsonResponse({"status" : "Id is required"})

class Completed(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        authorization = request.headers.get('Authorization').split()[1]
        username, password = b64decode(authorization).decode().split(':')
        user = authenticate(username=username, password=password)

        if user != None:
            tasks = Task.objects.filter(user=user, completed=True)
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
        return JsonResponse({"status": "Unauthorized"})

class Uncompleted(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        authorization = request.headers.get('Authorization').split()[1]
        username, password = b64decode(authorization).decode().split(':')
        user = authenticate(username=username, password=password)

        if user != None:
            tasks = Task.objects.filter(user=user, completed=False)
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

        return JsonResponse({'status': 'Unauthorized'})
