from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from aaa_doser.scripts.main import aaa_doser
from aaa_doser.serializers import predictAAASerializer

@permission_classes((permissions.AllowAny,))
class predictAAAView(APIView):
    serializer_class = predictAAASerializer
    def post(self, request, *args, **kwargs):
        t = float(request.data.get('contact_time'))
        c = float(request.data.get('concentration'))
        doser = aaa_doser()
        coverage = doser.interpolate(time=t, concentration=c)
        data = {
            "time": t,
            "concentration": c,
            "coverage": coverage}
        
        return Response(data=data)