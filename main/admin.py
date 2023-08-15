from django.contrib import admin
from .models import User,Category,Service,WeekDay,Room,RoomPhotos,Bron
# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(WeekDay)
admin.site.register(Service)
admin.site.register(Room)
admin.site.register(RoomPhotos)
admin.site.register(Bron)