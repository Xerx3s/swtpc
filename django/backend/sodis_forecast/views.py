from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from sodis_forecast.scripts.main import sodis_forecast
from sodis_forecast.serializers import SODISForecastSerializer

@permission_classes((permissions.AllowAny,))
class SODISForecastView(APIView):
    serializer_class = SODISForecastSerializer
    def post(self, request, *args, **kwargs):
        input_list = [
            str(request.data.get('latitude')),
            str(request.data.get('longitude')),
            int(request.data.get('starting_hour')),
            int(request.data.get('water_temperature')),
            int(request.data.get('target_logdis'))]

        result, message, duration = sodis_forecast(
            latlng=[input_list[0],input_list[1]],
            hour=input_list[2],
            wattemp=input_list[3],
            tarlogdis=input_list[4])
        data = {
            "latitude": input_list[0],
            "longitude": input_list[1],
            "starting_hour": input_list[2],
            "water_temperature": input_list[3],
            "target_logdis": input_list[4],
            "message": message,
            "duration": duration,
            "result": result}
        return Response(data=data)