from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main import views


router = DefaultRouter()
router.register(r'mails', views.MailViewSet, basename='mails')

urlpatterns = router.urls + [
    path('api-auth/', include('rest_framework.urls'))
]
