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
        cCl = float(request.data.get('concentration_chloride'))
        cSO4 = float(request.data.get('concentration_sulfate'))
        cHCO3 = float(request.data.get('concentration_bicarbonate'))
        cHPO4 = float(request.data.get('concentration_hydrogen_phosphate'))
        cAs = float(request.data.get('concentration_arsenic'))
        doser = aaa_doser()
        coverage = doser.interpolate(t, c, cCl, cSO4, cHCO3, cHPO4, cAs)
        data = {
            "concentration": c,
            "time": t,
            "cCl": cCl,
            "cSO4": cSO4,
            "cHCO3": cHCO3,
            "cHPO4": cHPO4,
            "cAs": cAs,
            "coverage": coverage}
        
        return Response(data=data)