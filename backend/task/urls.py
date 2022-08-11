from django.urls import path
from . import views

urlpatterns = [
    path('', views.gettasks, name="tasks"),
    path('post/', views.posttask, name="posttask"),
    path('edit/', views.edittask, name="edittask"),
    path('deactivate/', views.deactivatetask, name="deactivatetask"),
    path('activate/', views.activatetask, name="activatetask"),
    path('posttag/', views.posttag, name="posttag"),
    path('edittag/', views.edittag, name="edittag"),
]
