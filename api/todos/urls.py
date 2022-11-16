from django.urls import path, include #pulling in path form djang.urls
from .views import TodoAPIView, CategoryViewSet #pulling in the view we created
from rest_framework import routers #for modelviewset

#--ModelViewset-- ORDER MATTERS HERE
router = routers.SimpleRouter()
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('todo/', TodoAPIView.as_view()), #we have the path, using TodoAPIView as a view
    path('todo/<str:pk>/', TodoAPIView.as_view()), #captures primary key in the path
    path('', include(router.urls)), #for modelviewset, pulled from routers docs
]