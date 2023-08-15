from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
# from rsa import verify
from .serializer import *
from .errors import *
from .utils import *
from .msg import *

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = CreateUserProfileSerializer(data=request.data)
        if serializer.is_valid():
            verification_code = serializer.save(request.data)
            if verification_code is False:
                return MyResponse(error_status=INVALID_DATA,message=Message.PHONE_EXISTS) 

            request.session['verification_code'] = verification_code
            return MyResponse(error_status=SUCCESS,message=Message.USER_REGISTER_SUCCESSFULLY,verification_code=verification_code) 

        else:
            return MyResponse(error_status=INVALID_DATA,message=Message.INVALID_DATA,serializer_errors=serializer.errors) 



class ActivateView(APIView):
    permission_classes = [AllowAny]

    # Update verification code
    def get(self, request):
        try:
            p = User.objects.get(phone= request.data.get("phone"))    
        except:
            return MyResponse(error_status=INVALID_DATA,message=Message.USER_DOES_NOT_EXISTS) 
        p.verification_code = CreateVerificationCode()
        p.save()
        #  A verification code has been sent to the user's phone
        return MyResponse(error_status=SUCCESS,message=Message.VERIFATION_CODE_SEND,verification_code=p.verification_code,) 

    # User activate proccess

    def post(self, request):
        try:
            user = User.objects.get(phone=request.data.get("phone"))    
        except:
            return MyResponse(error_status=INVALID_DATA,message=Message.USER_DOES_NOT_EXISTS) 
        verification_code = request.data.get("verification_code")
        if str(verification_code) != str( user.verification_code):
            return MyResponse(error_status=INVALID_DATA,message=Message.USER_DOES_NOT_EXISTS) 
        else:
            user.is_active = True
            user.save()
            s = UserSerializer(user, many=False)
            t = Token.objects.get_or_create(user=user)
            register_date =  f"{user.date_joined.year},{user.date_joined.month}"
            return MyResponse(error_status=SUCCESS,message=Message.USER_ACTIVATED,serializer_objects=s.data,
                token=t[0].key ,register_date=register_date ) 

class LoginUser:
    def login_user(self, request):
        phone = request.data.get("phone")
        if phone is None:
            response = MyResponse(error_status=INVALID_DATA,message=Message.INVALID_DATA)
            return response
        
        try:
            profil =  User.objects.get(phone=phone)      
            profil.verification_code = CreateVerificationCode()
            profil.save()
            # profil.send_verification_code()
            response = MyResponse(error_status=SUCCESS,message=Message.VERIFATION_CODE_SEND,verification_code= profil.verification_code)
        except:
            response = MyResponse(error_status=INVALID_DATA,message=Message.INVALID_DATA)
        return response
      



class AuthorizationView(APIView,LoginUser):
    permission_classes = [AllowAny]

    def post(self, request):
        return self.login_user(request)
