from django.urls import path, include
from rest_framework_nested import routers
from .views import ChatMessageViewSet,ChatRoomViewSet,chat_test
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router = routers.SimpleRouter()
router.register(r'rooms',ChatRoomViewSet)

rooms_router = routers.NestedSimpleRouter(router, r'rooms', lookup='room')
rooms_router.register(r'messages', ChatMessageViewSet, basename='room-messages')


urlpatterns = [
    path('',include(router.urls)),
    path('',include(rooms_router.urls)),
    path('jwt/create/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('chat-test/<str:room_name>/', chat_test, name='chat-test'),

]

# router = DefaultRouter()
# router.register(r'messages',ChatMessageViewSet,basename='chatmessage')
# urlpatterns =[
#     path('',include(router.urls)),
#     path('chat-test/', chat_test, name='chat-test'),

# ]