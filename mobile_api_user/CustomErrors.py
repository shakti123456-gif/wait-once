
from rest_framework import status
from rest_framework.response import Response

class Error:
    def __init__(self,name):
        self.name=name

    @staticmethod
    def format_response(data, message='Request successful', status_code=status.HTTP_200_OK):
        response = {
            'status': 'success',
            'statusCode': status_code,
            'message': message,
            'data': data
        }
        return Response(response, status=status_code)
    
    @staticmethod
    def format_serializer_errors(serializer_errors, message='Validation error', status_code=status.HTTP_400_BAD_REQUEST):
        response = {
            'status': 'error',
            'statusCode': status_code,
            'message': message,
            'errors': serializer_errors
        }
        return Response(response, status=status_code)
    
    @staticmethod
    def invalid_creditials(self):
        pass 
    
    @staticmethod
    def application_flow(self):
        pass 

    @staticmethod
    def serialize_error(self):
        pass 



    