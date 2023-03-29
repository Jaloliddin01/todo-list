from django.urls import path
from .views import get_all, get_by_id, create, upadate_by_id, get_all_completed, get_all_uncompleted, delete_by_id, complete_by_id


urlpatterns = [
    path('tasks/', get_all),
    path('tasks/<int:id>/', get_by_id),
    path('tasks/create/', create),
    path('tasks/<int:id>/update/', upadate_by_id),
    path('tasks/<int:id>/delete/', delete_by_id),
    path('tasks/<int:id>/complete/', complete_by_id),
    path('tasks/completed/', get_all_completed),
    path('tasks/uncompleted/', get_all_uncompleted),
]