from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from floc_analyzer.scripts.useless_main import addTwoNumber
from floc_analyzer.serializers import TwoNumberSerializer

@permission_classes((permissions.AllowAny,))
class MyView(APIView):
    serializer_class = TwoNumberSerializer    
    def post(self, request, *args, **kwargs):
        my_result=addTwoNumber(float(request.data.get('firstnum')),float(request.data.get('secondnum')))
        return Response(data={"my_return_data":my_result})
