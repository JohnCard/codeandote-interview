from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "invalid JSON"}, status=400)

        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if user and user.is_superuser:
            login(request, user)  # Crea la sesión y cookie
            return JsonResponse({"message": "Success login ", "user": user.username})
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return JsonResponse({"message": "Logout successful"})