from main.models import * 
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from customer.utils import CreateVerificationCode
from django.contrib import messages
from django.db.models import Q
import datetime
from .send_bot import send

def register_(request):
    username = request.POST['username']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    phone = request.POST['phone']
    address= request.POST['address']
    password1= request.POST['password1']
    password2= request.POST['password2']

    if len(password1) < 8:
        print('parol 8 tadan kam bolmasligi kerak')
        # "password must be less than 8 characters"
        messages.error(request, "Parol 8 ta belgidan kam bo'lmasligi kerak !")
        return False

    if password1 != password2:
        print('parollar bir xil emas')
        # "Passwords is not equal"
        messages.error(request, "Parollar bir xil emas !")
        return False

    try:
        verification_code = CreateVerificationCode()
        user = User.objects.get(phone=phone)
        if user.is_active == False:
            user.verification_code=verification_code

            #send code
            send(phone,verification_code)
            print(f'{verification_code} kod yuborildi(try)')
        else:
            messages.error(request, "Siz oldin ro'yxatdan o'tgansiz !")
            return False
        request.session['phone'] = phone
        user.save()
        return True
    except:
        if User.objects.filter(username=username).exists():
            # "This username already exists"
            messages.error(request, "Bu username oldin ro'yxatdan o'tgan !")

            return False

        if User.objects.filter(phone=phone).exists():
            # "This phone already exists"
            messages.error(request, "Bu telefon raqam oldin ro'yxatdan o'tgan !")

            return False
        else:
            verification_code = CreateVerificationCode()
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                adres=address,
                password=password1,
                verification_code=verification_code,
                is_active=False,
            )
            request.session['phone'] = phone
            print(f'{verification_code} kod yuborildi(except)')
            print(f'{verification_code} kod yuborildi(except)')
            send(phone,verification_code)

        return True


def login_(request):
    username = request.POST['username']
    password = request.POST['password']

    if username and password:
            try:
                # user =  User.objects.get(username=username)
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request,user)
                    return True
            except:
                return False
    messages.error(request, "Login yoki parol xato !")


def checkVerification(request):
    phone = request.session['phone']
    ver_code = request.POST['ver_code']
    user = User.objects.filter(phone=phone)[0]
    if ver_code == user.verification_code:
        user.is_active =True
        user.save()
        return True
    messages.error(request, "Tasdiqlash kodi noto'g'ri kiritildi !")
    return False


def service_register(request):
    user = request.user
    user = User.objects.filter(username=user.username)[0]
    name = request.POST['name']
    adres = request.POST['adres']
    description = request.POST['description']
    img = request.FILES['img']
    category = request.POST['category']
    category = Category.objects.filter(name=category)[0]
    phone = request.POST['phone']
    phone_2 = request.POST['phone_2']
    working_time_from = request.POST['working_time_from']
    working_time_to = request.POST['working_time_to']
    working_days = request.POST['working_days']
    working_day = WeekDay.objects.filter(day_name=working_days)[0]
    open_service = request.POST['open_service']
    open_service = True if open_service == '1' else False
    service = Service.objects.create(owner=user,
                                        name=name,
                                        adres=adres,
                                        description=description,
                                        image = img,
                                        category=category,
                                        phone=phone,
                                        phone_2=phone_2,
                                        working_time_from=working_time_from,
                                        working_time_to=working_time_to,
                                        open_service=open_service)

    service.working_days.add(working_day)
    # service = messages.error(request, " hatolik yuzberdi ")  if service  else messages.error(request, " hatolik yuzberdi ")
    service = True if service  else False
    return service

def service_update(request,pk):
    user = request.user
    user = User.objects.filter(username=user.username)[0]
    service = Service.objects.get(id=pk)
    
    name = request.POST['name']
    adres = request.POST['adres']
    description = request.POST['description']
    img = request.FILES['img']
    category = request.POST['category']
    category = Category.objects.filter(name=category)[0]
    phone = request.POST['phone']
    phone_2 = request.POST['phone_2']
    working_time_from = request.POST['working_time_from']
    working_time_to = request.POST['working_time_to']
    working_days = request.POST['working_days']
    # working_day = WeekDay.objects.filter(day_name=working_days)[0]
    open_service = request.POST['open_service']
    open_service = True if open_service == '1' else False

    service.owner=user
    service.name=name
    service.adres=adres
    service.description=description
    service.category=category
    service.phone=phone
    service.phone_2=phone_2
    service.working_time_from=working_time_from
    service.working_time_to=working_time_to
    service.open_service=open_service

    # service.working_days.update(day_name = working_day.day_name)
    service.image = img
    service.working_days.update(day_name = working_days)
    # service = messages.error(request, " hatolik yuzberdi ")  if service  else messages.error(request, " hatolik yuzberdi ")
    service.save()

    return True

def room_create(request,pk):
    service = Service.objects.get(id = int(pk))
    name =request.POST['name']
    size =request.POST['size']
    owner =request.POST['owner']
    adres =request.POST['adres']
    description =request.POST['description']
    room = Room.objects.create(
        service=service,
        name=name,
        size=size,
        owner=owner,
        adres=adres,
        description=description

    )
    room = True if room else False
    return room

def room_update(request,pk):
    try:
        name =request.POST['name']
        size =request.POST['size']
        owner =request.POST['owner']
        adres =request.POST['adres']
        room = Room.objects.get(id = int(pk))
        room.name = name
        room.size = size
        room.owner = owner
        room.adres = adres
        room.save()
        return True
    except:
        return False
def img_create(request,pk):
    try:
        image = request.FILES['image']
        room = Room.objects.get(id=int(pk))
        # room =  room.room_photos.create(image=image)
        room  = RoomPhotos.objects.create(room=room, image=image)
        print(room)
        print(image)
        print(room)
        if room :
            return True
    except:
        return False
    
def addBron(request):
    
    try:
        room_id = request.POST['room']
        room = Room.objects.filter(id=room_id)[0]
    except:
        room_id = request.POST['room_']
        room = Room.objects.filter(id=room_id)[0]
        
    customer = request.user
    name = request.POST['name']
    phone = request.POST['phone']
    time_from = request.POST['bron_time_from']
    time_to = request.POST['bron_time_to']
    date = request.POST['date']

    bron = Bron.objects.filter(
                        Q(room=room,date=date, time_from__range=(time_from[:4]+'1',time_to),status='waiting' )
                        |Q(room=room,date=date, time_to__range=(time_from[:4]+'1',time_to), status='waiting' )
                        |Q(room=room,date=date, time_from__lte = time_from ,time_to__gte = time_to, status='waiting' )

                        ).exists()

    if bron:
        bron = Bron.objects.filter(room=room,date=date)
        return bron
    bron = Bron.objects.create(
        room=room,
        customer = customer,
        time_from=time_from,
        time_to=time_to,
        date=date,
        name=name,
        phone=phone,
        )    

    return [True,room]

def cancelBron(request):
    now = datetime.datetime.today()
    id_bron = request.POST['id_bron']
    canceller = request.POST['canceller']
    bron = Bron.objects.get(id=id_bron)
    bron.canceller = canceller
    bron.cancel_date = now
    bron.status = 'cancelled'
    bron.save()
    return bron
    
    
def profilUpdate(request):
    username = request.POST['username']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    phone = request.POST['phone']
    adres= request.POST['address']
    password1= request.POST.get('password1', False)
    password2= request.POST.get('password1', False)
    
    try:
        profil = request.user
        user = User.objects.get(username=profil)
    except:
        pass
    
    if password1 != False:
        if len(password1) < 8:
            print('parol 8 tadan kam bolmasligi kerak')
            # "password must be less than 8 characters"
            messages.error(request, "Parol 8 ta belgidan kam bo'lmasligi kerak !")
            return False

        if password1 != password2:
            print('parollar bir xil emas')
            # "Passwords is not equal"
            messages.error(request, "Parollar bir xil emas !")
            return False
        
        user.set_password(password1)
        
    user.username = username
    user.first_name = first_name
    user.last_name = last_name
    user.phone = phone
    user.adres = adres
    user.email = email
    user.save()

    return True
    
    
def infoBrons(request):
    pk = request.GET['pk']
    day = request.GET['day']
    month = request.GET['month']
    year = request.GET['year']
    date = datetime.date(int(year),int(month),int(day))
    bron = Bron.objects.filter(room__service=pk, date=date)
    return bron

def updateBrons(request,pk):
    room_id = request.POST['room']
    name = request.POST['name']
    phone = request.POST['phone']
    time_from = request.POST['bron_time_from']
    time_to = request.POST['bron_time_to']
    date = request.POST['date']
    
    if int(time_from[:2]) >= int(time_to[:2]):
        return False

    room = Room.objects.filter(id=room_id)[0]
    
    update_bron = Bron.objects.get(id=pk)   


    bron = Bron.objects.filter(
                        Q(room=room,date=date, time_from__range=(time_from[:4]+'1',time_to),status='waiting' )
                        |Q(room=room,date=date, time_to__range=(time_from[:4]+'1',time_to), status='waiting' )
                        |Q(room=room,date=date, time_from__lte = time_from ,time_to__gte = time_to, status='waiting' )

                        ).exists()

    if bron:
        bron = Bron.objects.filter(room=room,date=date)
        return bron
    else:
        update_bron.room = room
        update_bron.name = name
        update_bron.phone = phone
        update_bron.time_from = time_from
        update_bron.time_to = time_to
        update_bron.date = date
        update_bron.save()
        
 

    return True

def uzbekWeekdays(date_):
    day = date_.strftime("%a")
    month = date_.strftime("%b")
    week_days = {
        "Mon":"Dushanba",
        "Tue":"Seshanba",
        "Wed":"Chorshanba",
        "Thu":"Payshanba",
        "Fri":"Juma",
        "Sat":"Shanba",
        "Sun":"Yakshaba"
    }
    
    months = {
        "Jan":"Yanvar",
        "Feb":"Fevral",
        "Mar":"Mart",
        "Apr":"Aprel",
        "May":"May",
        "Jun":"Iyun",
        "Jul":"Iyul",
        "Aug":"Avgust",
        "Sep":"Sentabr",
        "Oct":"Oktabr",
        "Dec":"Dekabr"
    }

    c = {
        day:week_days[day],
        month:months[month]
    }
    
    return c


def delete_room(request ,pk):
    room = Room.objects.get(id = int(pk) ).delete()
    return True
def delete_image(request , pk):
    image = RoomPhotos.objects.get(id = int(pk)).delete()
    return True
