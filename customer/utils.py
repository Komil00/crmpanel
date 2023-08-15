from rest_framework.response import Response
import random 
from main.models import User

class MyResponse(Response):
    
    def __init__(self,error_status, serializer_objects=None, message=None, status=None, template_name=None, 
        headers=None, exception=False, content_type=None,**kwargs):
        data = {
            "error_status":error_status,
            "message":message,
        }
        if kwargs.get('serializer_errors'):
            data['erros'] = kwargs.get('serializer_errors')
            kwargs.pop('serializer_errors')
        for k,v in kwargs.items():
            data[k] = str(v)
        if serializer_objects:
            data['data'] = serializer_objects
        super().__init__(data, status, template_name, headers, exception, content_type)

def CreateVerificationCode():
    ver_code_numbers = []
    for x in range(5):
        number = random.randint(1,9)
        ver_code_numbers.append(str(number))
    return "".join(ver_code_numbers)



   