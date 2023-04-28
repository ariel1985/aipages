from django.urls import path
from . import views

app_name = 'home' # for namespace in urls

urlpatterns = [
    # path('urlparamnamehere', views.index, name='name used in links'),
    path('', views.index, name='index'),
]
