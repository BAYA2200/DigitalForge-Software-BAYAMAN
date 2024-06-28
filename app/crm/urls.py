from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterManagerView, ManagerUserListView, ManagerUserDetailView, \
    ManagerUserUpdateView, ManagerUserDeleteView, ApartmentViewSet, ClientViewSet, ObtainJWTView

router = DefaultRouter()
router.register(r'apartments', ApartmentViewSet)
router.register(r'clients', ClientViewSet)

urlpatterns = [
    path('register/', RegisterManagerView.as_view(), name='register_manager'),
    path('login/', ObtainJWTView.as_view(), name='login_manager'),
    path('managers/', ManagerUserListView.as_view(), name='list_managers'),
    path('managers/<int:pk>/', ManagerUserDetailView.as_view(), name='detail_manager'),
    path('managers/<int:pk>/update/', ManagerUserUpdateView.as_view(), name='update_manager'),
    path('managers/<int:pk>/delete/', ManagerUserDeleteView.as_view(), name='delete_manager'),
    path('', include(router.urls)),
]
