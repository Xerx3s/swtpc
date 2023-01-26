from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from floc_analyzer.scripts.main import outputprediction, inputoptimization
from floc_analyzer.serializers import predictECSerializer, predictpHSerializer, predictTurSerializer, optimizeTurSerializer
from floc_analyzer.models import get_floc, get_sw, get_bounds

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
class list_bounds(APIView):
    def get(self, request, *args, **kwargs):
        data = get_bounds()
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

@permission_classes((permissions.AllowAny,))
class optimizeTurView(APIView):
    serializer_class = optimizeTurSerializer
    def post(self, request, *args, **kwargs):
        input_list = [
            float(request.data.get("initial_pH_min")),
            float(request.data.get("initial_pH_max")),
            int(request.data.get("initial_EC_min")),
            int(request.data.get("initial_EC_max")),
            int(request.data.get("initial_turbidity_min")),
            int(request.data.get("initial_turbidity_max")),
            int(request.data.get("floc_concentration_min")),
            int(request.data.get("floc_concentration_max")),
            float(request.data.get("floc_saline_Molarity_min")),
            float(request.data.get("floc_saline_Molarity_max")),
            int(request.data.get("floc_dose_min")),
            int(request.data.get("floc_dose_max")),
            int(request.data.get("floc_cactus_share_min")),
            int(request.data.get("floc_cactus_share_max")),
            int(request.data.get("stirring_speed_coagulation_phase_min")),
            int(request.data.get("stirring_speed_coagulation_phase_max")),
            int(request.data.get("duration_coagulation_phase_min")),
            int(request.data.get("duration_coagulation_phase_max")),
            int(request.data.get("stirring_speed_flocculation_phase_min")),
            int(request.data.get("stirring_speed_flocculation_phase_max")),
            int(request.data.get("duration_flocculation_phase_min")),
            int(request.data.get("duration_flocculation_phase_max")),
            int(request.data.get("duration_sedimentation_phase_min")),
            int(request.data.get("duration_sedimentation_phase_max"))
        ]

        bounds_dict = {
            "initial_pH": [input_list[0], input_list[1]],
            "initial_EC": [input_list[2], input_list[3]],
            "initial_turbidity": [input_list[4], input_list[5]],
            "floc_concentration": [input_list[6], input_list[7]],
            "floc_saline_Molarity": [input_list[8], input_list[9]],
            "floc_dose": [input_list[10], input_list[11]],
            "floc_cactus_share": [input_list[12], input_list[13]],
            "stirring_speed_coagulation_phase": [input_list[14], input_list[15]],
            "duration_coagulation_phase": [input_list[16], input_list[17]],
            "stirring_speed_flocculation_phase": [input_list[18], input_list[19]],
            "duration_flocculation_phase": [input_list[20], input_list[21]],
            "duration_sedimentation_phase": [input_list[22], input_list[23]],
        }
            
        output, best_param = inputoptimization(
            bounds=bounds_dict,
            pred_type=request.data.get("pred_type"),
            floc=request.data.get("flocculant"),
            loadpipe=request.data.get('load_pipe'),
            printass=request.data.get('print_assessment'))

        if request.data.get("pred_type") == "ec":
            data = {
                "initial_EC": best_param[0],
                "flocculant": request.data.get("flocculant"),
                "floc_concentration": best_param[1],
                "floc_saline_Molarity": best_param[2],
                "floc_dose": best_param[3],
                "floc_vol": best_param[4],
                "saline concentration": best_param[5],
                "final_EC": output}
        elif request.data.get("pred_type") == "ph":
            data = {
                "initial_pH": best_param[0],
                "flocculant": request.data.get("flocculant"),
                "floc_concentration": best_param[1],
                "floc_saline_Molarity": best_param[2],
                "floc_dose": best_param[3],
                "final_pH": output}

        elif request.data.get("pred_type") == "tur":
            data = {
                "initial_pH": best_param[0],
                "initial_EC": best_param[1],
                "initial_turbidity": best_param[2],
                "flocculant": request.data.get("flocculant"),
                "floc_saline_Molarity": best_param[3],
                "floc_dose": best_param[4],
                "floc_cactus_share": best_param[5],
                "stirring_speed_coagulation_phase": best_param[6],
                "duration_coagulation_phase": best_param[7],
                "stirring_speed_flocculation_phase": best_param[8],
                "duration_flocculation_phase": best_param[9],
                "duration_sedimetation_phase": best_param[10],
                "final_turbidity": output}

        return Response(data=data)