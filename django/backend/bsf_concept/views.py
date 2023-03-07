from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from bsf_concept.scripts.main import outputprediction, inputoptimization
from bsf_concept.serializers import predictBsfSerializer, optimizeBsfSerializer
from bsf_concept.models import get_bounds, get_materials

@permission_classes((permissions.AllowAny,))
class list_bsf_bounds(APIView):
    def get(self, request, *args, **kwargs):
        data = get_bounds()
        return Response(data=data)

@permission_classes((permissions.AllowAny,))
class list_bsf_materials(APIView):
    def get(self, request, *args, **kwargs):
        data = get_materials()
        return Response(data=data)

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


@permission_classes((permissions.AllowAny,))
class optimizeBsfView(APIView):
    serializer_class = optimizeBsfSerializer
    def post(self, request, *args, **kwargs):
        input_list = [
            int(request.data.get("diameter_min")),
            int(request.data.get("diameter_max")),
            float(request.data.get("material_height_min")),
            float(request.data.get("material_height_max")),
            float(request.data.get("mean_grain_diameter_max")),
            float(request.data.get("mean_grain_diameter_max")),
            float(request.data.get("mean_flow_min")),
            float(request.data.get("mean_flow_max")),
            int(request.data.get("mean_pause_min")),
            int(request.data.get("mean_pause_max")),
            int(request.data.get("time_schmutzdecke_min")),
            int(request.data.get("time_schmutzdecke_max")),
            int(request.data.get("initial_turbidity_min")),
            int(request.data.get("initial_turbidity_max"))
        ]

        bounds_dict = {
            "diameter": [input_list[0], input_list[1]],
            "material_height": [input_list[2], input_list[3]],
            "mean_grain_diameter": [input_list[4], input_list[5]],
            "mean_flow": [input_list[6], input_list[7]],
            "mean_pause": [input_list[8], input_list[9]],
            "time_schmutzdecke": [input_list[10], input_list[11]],
            "initial_turbidity": [input_list[12], input_list[13]]
        }
            
        output, best_param = inputoptimization(
            bounds=bounds_dict,
            loadpipe=request.data.get('load_pipe'),
            printass=request.data.get('print_assessment')
        )

        data = {
            "diameter": best_param[0],
            "material_height": best_param[1],
            "mean_grain_diameter": best_param[2],
            "mean_flow": best_param[3],
            "mean_pause": best_param[4],
            "time_schmutzdecke": best_param[5],
            "initial_turbdity": best_param[6],
            "final_turbidity": output
        }

        return Response(data=data)