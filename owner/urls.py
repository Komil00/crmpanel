from django.urls import path
from .views import *
from django.conf.urls import handler404,handler500

from django.views import static

app_name = 'owner'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('logout', logout_, name='log_out'),
    path('profil', OwnerProfilView.as_view(), name='owner_profil'),
    path('intro', IntroView.as_view(), name='intro'),
    path('verification', VerificationView.as_view(), name='verification'),
    path('service' , ServiceView.as_view(),name = 'service'),
    path('service/<int:pk>' , ServiceDetailView.as_view(),name = 'service_detail'),
    path('room_create/<int:pk>' , RoomView.as_view(),name = 'room_create'),
    path('room/<int:pk>',RoomView.as_view(),name = 'room'),
    path('room/update/<int:pk>',RoomUpdateView.as_view(),name = 'room_update'),
    path('brons/<int:pk>',BronView.as_view(),name = 'brons'),
    path('calendar/<int:pk>',calendar_view,name = 'calendar'),
    path('add/bron/',BronAddView.as_view(),name = 'add_bron'),
    path('cancel/bron',BronCancelView.as_view(),name = 'cancel_bron'),
    path('infoBrons', InfoBrons.as_view(),name='info_brons'),
    path('updateBron/<int:pk>', CalendarUpdateBron.as_view(),name='update_bron'),
    path('get/room', get_room,name='get_room'),
    path('delete_room/<int:pk>/<int:id_service>' , DeleteRoomView.as_view() , name = "delete_room"),
    path('delete_image/<int:pk>/<int:id_room>' , DeleteImageView.as_view() , name= "delete_image" )
    
]

handler404=handler_404
handler500=handler_500
