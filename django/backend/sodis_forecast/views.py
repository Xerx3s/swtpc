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
            str(request.data.get('location_city')),
            str(request.data.get('location_country')),
            int(request.data.get('starting_hour')),
            int(request.data.get('water_temperature')),
            int(request.data.get('target_logdis'))]
        location = {"city": input_list[0], "country": input_list[1]}

        result, message =sodis_forecast(
            location=location,
            hour=input_list[2],
            wattemp=input_list[3],
            tarlogdis=input_list[4])
        data = {
            "location": location,
            "starting_hour": input_list[2],
            "water_temperature": input_list[3],
            "target_logdis": input_list[4],
            "message": message,
            "result": result}
        return Response(data=data)