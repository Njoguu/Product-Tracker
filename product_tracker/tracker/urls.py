from django.urls import path
from .views import index

urlpatterns = [
    path("", view=index, name="index")
]