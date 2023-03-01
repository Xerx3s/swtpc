from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from bsf_concept.scripts.main import outputprediction, inputoptimization
from bsf_concept.serializers import predictBsfSerializer

@permission_classes((permissions.AllowAny,))
class predictBsfView(APIView):
    serializer_class = predictBsfSerializer
    def post(self, request, *args, **kwargs):
        input_list = [
            int(request.data.get('diameter')),
            float(request.data.get('material_height')),
            float(request.data.get('mean_grain_diameter')),
            float(request.data.get('mean_flow')),
            int(request.data.get('mean_pause')),
            int(request.data.get('time_schmutzdecke')),
            int(request.data.get('initial_turbidity'))
        ]
        result=outputprediction(
            input_list,
            loadpipe=request.data.get('load_pipe'),
            printass=request.data.get('print_assessment'))
        data = {
            "diameter": input_list[0],
            "material_height": input_list[1],
            "mean_grain_diameter": input_list[2],
            "mean_flow": input_list[3],
            "mean_pause": input_list[4],
            "time_schmutzdecke": input_list[5],
            "final_turbidity": result}
        return Response(data=data)