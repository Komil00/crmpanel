from django.shortcuts import render, redirect
from django.views import View
from .tools import *
from main.models import *
from .decorators import deco_login
import datetime
from django.http import JsonResponse



# Create your views here.

today = datetime.datetime.now()
class HomeView(View):
    @deco_login
    def get(self, request):
        category = Category.objects.all()
        weekday = WeekDay.objects.all()
        context ={
            'category':category,
            'weekday' :weekday,
        }
        try:
            service = Service.objects.filter(owner=request.user)
            context['service'] = service
        except:
            pass
        return render(request,'index.html', context)



class LoginView(View):
    def get(self, request):
        return render(request,'login.html')

    def post(self, request):
        login = login_(request)
        if login:
            return redirect('/')
        print('xato login view')
        return render(request,'login.html')

def logout_(request):
    logout(request)
    return redirect('owner:login')

class RegisterView(View):
    def get(self, request):
        return render(request,'register.html')

    def post(self, request):
        register = register_(request)
        if register:
            return redirect('/verification')
        print('xato')
        return render(request,'register.html')

class VerificationView(View):
    def get(self, request):
        return render(request,'verification.html')

    def post(self, request):
        v = checkVerification(request)
        if v:
            return redirect('/')
        return render(request,'verification.html')

class IntroView(View):
    def get(self,request):
        return render(request,'intro.html')


class ServiceView(View):

    def post(self,request):
        service =  service_register(request)
        if service == True:
            return redirect('/')
        return redirect('/')

class ServiceDetailView(View):

    def get(self, request,pk):
        category = Category.objects.all()
        weekday = WeekDay.objects.all()
        service = Service.objects.get(id=pk)
        rooms = Room.objects.filter(service=service)
        
        context = {
            'category':category,
            'weekday':weekday,
            'service':service,
            'rooms':rooms,
            "today":today.date
        }
        return render(request,'detail_service.html', context)
        
    def post(self, request,pk):
        service =  service_update(request,pk)
        if service == True:
            return redirect(f'/service/{pk}')
        return redirect('/')


class RoomView(View):

    def post(self,request ,pk):
        room  = room_create(request ,pk)
        if room == True:
            return redirect(f'/service/{pk}')
        return redirect(f'/service/{pk}')



class RoomUpdateView(View):
    @deco_login
    def get(self,request,pk):
        room = Room.objects.get(id=int(pk))
        # image = room.room_photos.all()

        context = {'room':room,
                   }
        return render(request,'room_parametr.html',context)
    def post(self,request,pk):
      
        update = room_update(request,pk)
        if update:
            return redirect(f"/room/update/{pk}")
        img  =  img_create(request,pk)
        if img:
            return redirect(f"/room/update/{pk}")
        print("xatooooo")
        return redirect(f"/room/update/{pk}")

class BronView(View):
    def get(self,request, pk):
        service = Service.objects.get(pk=pk)
        return render(request, 'fullcalendar.html', {"service":service})
    
def calendar_view(request, pk):
    rooms = Room.objects.filter(service=pk)
    events = []
    for r in rooms:
        brons = Bron.objects.filter(room=r.id)
        for bron in brons:
            if bron.status != 'cancelled':
                f = bron.time_from.strftime("%H:%M")
                e = bron.time_to.strftime("%H:%M")
                event = {
                    'id': r.id,
                    'title': f'{bron.room.name} { f }-{ e }',
                    'start': f"{bron.date}T{bron.time_from}",
                    'end': f"{bron.date}T{bron.time_to}",
                    'className': 'success',
                    'allDay': False,
                }
                events.append(event)
        
    data  = {
        "data":events
    }
    return JsonResponse(data)




    
    
class BronAddView(View):
    def get(self, request):
        services= Service.objects.filter(owner=request.user)
        # room =  Room.objects.filter(service=pk)
        # context = {
        #     "rooms":room,
        #     "pk":pk
        # }
        context = {
            "services":services
        }
        return render(request, 'add_bron.html', context)
    
    def post(self, request):
        
        bron = addBron(request)
        if bron[0] == True:
            messages.success(request, "Xona muvaffaqiyatli band qilindi !")
        else:
            for i in bron:
                messages.error(request, f"Ushbu xona {i.date} kuni {str(i.time_from)[:5]} dan {str(i.time_to)[:5]} gacha band !")
        # room =  Room.objects.filter(service=pk)
        services = Service.objects.filter(owner=request.user)

        context = {
            "services":services,
            
        }

        return redirect(f'/brons/{bron[1].service.id}')
    


class OwnerProfilView(View):
    @deco_login
    def get(self, request):
        user = User.objects.filter(username=request.user)[0]
        return render(request, 'owner_profil.html',{"user":user})
    
    def post(self, request):
        profilUpdate(request)
        return redirect('/profil')
    
class BronCancelView(View):
    def post(self, request):
        service_id = int(request.POST['id_service'])
        cancelBron(request)
        return redirect(f'/service/{service_id}')
    
    
class InfoBrons(View):
    def get(self, request):
        pk = request.GET['pk']
        day = request.GET['day']
        month = request.GET['month']
        year = request.GET['year']
        brons = infoBrons(request)
        
        rooms = Room.objects.filter(service=pk)
        
        print(rooms)
        print(rooms)
        print(rooms)
        
        date_ = datetime.date(int(year),int(month),int(day))
        day = date_.strftime("%a")
        month = date_.strftime("%b")
         
        uz = uzbekWeekdays(date_)
    
        d = request.session['date'] = f"pk={pk}&day={day}&month={month}&year={year}"
      
        return render(request, "detail_calendar.html",{"brons":brons, "rooms":rooms,"service_pk":pk, "date":date_, "day":uz[day], "month":uz[month]})
    
    def post(self,request):
        d = request.session['date']
        cancelBron(request)
        messages.success(request, "Bron bekor qilindi !")

        return redirect(f"/infoBrons?{d}")
    
    
    
class CalendarUpdateBron(View):
    def post(self, request,pk):
        d = request.session['date']
        
        update_bron = updateBrons(request,pk)
        if update_bron == True:
            messages.success(request, "Muvaffaqiyatli o'zgartirildi !")
        elif update_bron == False:
            messages.error(request, "Vaqtni belgilashda xatolik !")
        else:
            messages.error(request, "Band qilingan! Boshqa vaqtni tanlang")
            
        
        return redirect(f"/infoBrons?{d}")
        
def get_room(request):
    service = request.GET['service']
    all_rooms = []
    rooms = Room.objects.filter(service=service)
    
    for r in rooms:
        rooms_ = {
                'id': r.id,
                "name":r.name
                }
        all_rooms.append(rooms_)
        
    
    return JsonResponse({"status":"ok","all_rooms":all_rooms})
         
         

def handler_404(request,exception):
    return render(request, "404.html")

def handler_500(request):
    return render(request, "500.html")

 
class DeleteRoomView(View):
    def get(self , request , pk , id_service):
        room = delete_room(request , pk)
        messages.add_message(request , messages.SUCCESS , "XONA OCHIRILDI !")
        return redirect(f"/service/{id_service}")
class DeleteImageView(View):
    def get(self , request , pk , id_room):
        image = delete_image(request , pk)
        room = Room.objects.get(id = int(id_room))
        messages.add_message(request , messages.SUCCESS , "RASM OCHIRILDI !")
        return redirect(f"/room/update/{id_room}")

        
    
