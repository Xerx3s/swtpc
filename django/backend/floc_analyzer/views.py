from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from floc_analyzer.scripts.new_main import outputprediction
from floc_analyzer.serializers import predictECSerializer, predictpHSerializer, predictTurSerializer
from floc_analyzer.models import get_floc, get_sw

@permission_classes((permissions.AllowAny,))
class list_surface_waters(APIView):
    def get(self, request, *args, **kwargs):
        data = get_sw()
        return Response(data=data)

@permission_classes((permissions.AllowAny,))
class list_flocculants(APIView):
    def get(self, request, *args, **kwargs):
        data = get_floc()
        return Response(data=data)

@permission_classes((permissions.AllowAny,))
class predictEcView(APIView):
    serializer_class = predictECSerializer
    def post(self, request, *args, **kwargs):
        input_list = [
            int(request.data.get('initial_EC')),
            float(request.data.get('floc_concentration')),
            float(request.data.get('floc_saline_Molarity')),
            int(request.data.get('floc_dose'))]
        input_list.append(input_list[3]/input_list[1]),
        input_list.append(input_list[4]*input_list[2])
        result=outputprediction(
            input_list,
            pred_type="ec",
            loadpipe=request.data.get('load_pipe'),
            printass=request.data.get('print_assessment'))
        data = {
            "initial_EC": input_list[0],
            "floc_concentration": input_list[1],
            "floc_saline_Molarity": input_list[2],
            "floc_dose": input_list[3],
            "floc_vol": input_list[4],
            "saline concentration": input_list[5],
            "final_EC": result}
        return Response(data=data)

@permission_classes((permissions.AllowAny,))
class predictPhView(APIView):
    serializer_class = predictpHSerializer
    def post(self, request, *args, **kwargs):
        input_list = [
            float(request.data.get('initial_pH')),
            float(request.data.get('floc_concentration')),
            float(request.data.get('floc_saline_Molarity')),
            int(request.data.get('floc_dose'))]
        result=outputprediction(
            input_list,
            pred_type="ph",
            loadpipe=request.data.get('load_pipe'),
            printass=request.data.get('print_assessment'))
        data = {
            "initial_pH": input_list[0],
            "floc_concentration": input_list[1],
            "floc_saline_Molarity": input_list[2],
            "floc_dose": input_list[3],
            "final_pH": result}
        return Response(data=data)

@permission_classes((permissions.AllowAny,))
class predictTurView(APIView):
    serializer_class = predictTurSerializer
    def post(self, request, *args, **kwargs):
        input_list = [
            float(request.data.get("initial_pH")),
            int(request.data.get("initial_EC")),
            int(request.data.get("initial_turbidity")),
            float(request.data.get("floc_saline_Molarity")),
            int(request.data.get("floc_dose")),
            int(request.data.get("floc_cactus_share")),
            int(request.data.get("stirring_speed_coagulation_phase")),
            int(request.data.get("duration_coagulation_phase")),
            int(request.data.get("stirring_speed_flocculation_phase")),
            int(request.data.get("duration_flocculation_phase")),
            int(request.data.get("duration_sedimentation_phase"))]
        result=outputprediction(
            inputvalues=input_list,
            pred_type="tur",
            floc=request.data.get("flocculant"),
            loadpipe=request.data.get('load_pipe'),
            printass=request.data.get('print_assessment'))
        data = {
            "initial_pH": input_list[0],
            "initial_EC": input_list[1],
            "initial_turbidity": input_list[2],
            "flocculant": request.data.get("flocculant"),
            "floc_saline_Molarity": input_list[3],
            "floc_dose": input_list[4],
            "floc_cactus_share": input_list[5],
            "stirring_speed_coagulation_phase": input_list[6],
            "duration_coagulation_phase": input_list[7],
            "stirring_speed_flocculation_phase": input_list[8],
            "duration_flocculation_phase": input_list[9],
            "duration_sedimetation_phase": input_list[10],
            "final_turbidity": result}
        return Response(data=data)