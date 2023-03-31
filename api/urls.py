from django.urls import path
from .views import Tasks, Tasks_id, Tasks_create, Complete, Completed, Uncompleted, Registration


urlpatterns = [
    path('user/', Registration.as_view()),
    path('tasks/<int:id>/', Tasks.as_view()),
    path('tasks/', Tasks.as_view()),
    path('tasks/create/', Tasks_create.as_view()),
    path('tasks/<int:id>/update/', Tasks.as_view()),
    path('tasks/<int:id>/delete/', Tasks.as_view()),
    path('tasks/<int:id>/complete/', Complete.as_view()),
    path('tasks/completed/', Completed.as_view()),
    path('tasks/uncompleted/', Uncompleted.as_view()),
]