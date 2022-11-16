from django.urls import path #pulling in path form djang.urls
from .views import TodoAPIView #pulling in the view we created

urlpatterns = [
    path('todo/', TodoAPIView.as_view()), #we have the path, using TodoAPIView as a view
    path('todo/<str:pk>/', TodoAPIView.as_view()), #captures primary key in the path
]