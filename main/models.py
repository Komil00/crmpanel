from django.contrib.auth.models import AbstractUser
from .choicetypes import *
# Create your models here.



class User(AbstractUser):
    phone = models.CharField("Telefoni",max_length=14, unique=True, db_index=True)
    user_type = models.CharField("Turi",choices=UserType.choices, max_length=14)
    user_status = models.CharField("Statusi",choices=UserStatusType.choices, max_length=14,blank=True)
    adres = models.TextField("Manzili")
    lat = models.FloatField(blank=True,null=True,default=0.0)
    long = models.FloatField(blank=True,null=True,default=0.0)
    verification_code = models.CharField(default=564879,max_length=8,blank=True)


class Category(models.Model):
    name = models.CharField("Nomi",max_length=20)

    def __str__(self) -> str:
        return self.name


class WeekDay(models.Model):
    day_name = models.CharField("Nomi",max_length=20)
    day_number = models.IntegerField()


    def __str__(self) -> str:
        return self.day_name


class Service(models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_services')
    name = models.CharField("Nomi",max_length=200)
    adres = models.TextField("Manzili")
    description = models.TextField("Servis xaqida" , blank=True)
    image = models.ImageField(upload_to="service_photos", blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='services')
    phone = models.CharField("Telefoni",max_length=14)
    phone_2 = models.CharField("Qo'shimcha Telefoni",max_length=14,blank=True)
    working_time_from = models.TimeField(blank=True)
    working_time_to = models.TimeField(blank=True)
    working_days = models.ManyToManyField(WeekDay)
    lat = models.FloatField(blank=True,null=True,default=0.0)
    long = models.FloatField(blank=True,null=True,default=0.0)
    rating = models.IntegerField(default=0)
    open_service = models.BooleanField(default=False)
    comments_count = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.name

class Room(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service_rooms')
    name = models.CharField("Nomi Masalan (1-xona)",max_length=200)
    owner = models.CharField("Xona egasi", max_length=200)
    adres = models.TextField("Manzili")
    size = models.PositiveIntegerField(default=0)
    description = models.TextField("Xona xaqida" , blank=True)
    rating = models.IntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    
    def __str__(self) -> str:
        return self.name

class RoomPhotos(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_photos')
    image = models.ImageField(upload_to="room_photos")
  

class ServicePhotos(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service_photos')
    image = models.ImageField(upload_to="service_photos")


class Bron(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_brons')
    customer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_brons')
    date = models.DateField("sana")
    time_from = models.TimeField(blank=True)
    time_to = models.TimeField(blank=True)
    status = models.CharField("Statusi",choices=BronStatus.choices, max_length=20,default=BronStatus.waiting)
    canceller = models.CharField("Bronni bekor qiluvchi",choices=CancellerType.choices,
    max_length=20,blank=True, null=True)
    cancel_date = models.DateTimeField(blank=True, null=True)
    name = models.CharField("Kimni nomiga", max_length=50, null=True, blank=True)
    phone = models.CharField("Telefon raqami", max_length=13, null=True, blank=True)
    
    reg_date = models.DateTimeField(auto_now_add=True)



    



