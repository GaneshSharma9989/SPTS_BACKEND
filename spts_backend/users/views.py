from django.shortcuts import render
import secrets
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
import json
User = get_user_model()
TOKENS = {}
@csrf_exempt
def get_users(request):
    if request.method == "GET":
        users = User.objects.all().values("id", "username", "email", "role")
        return JsonResponse(list(users), safe=False)

    return JsonResponse({"message": "Only GET method allowed"}, status=405)

@csrf_exempt
def register_teacher(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            if not username or not email or not password:
                return JsonResponse({'error': 'All fields are required'}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)

            user = User.objects.create(
                username=username,
                email=email,
                 password=make_password(password),
                role='teacher'
            )
            return JsonResponse({'message': 'Teacher registered successfully'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

@csrf_exempt
def login_teacher(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            print("Raw request body:", body)

            data = json.loads(body)
            print("Parsed JSON:", data)

            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse({'error': 'Username and password are required'}, status=400)

            user = authenticate(username=username, password=password)
            print("Authenticated user:", user)

            if user and user.role == 'teacher':
                from .utils import generate_token
                token = generate_token(user)
                print("Generated token:", token)
                return JsonResponse({'token': token})

            return JsonResponse({'error': 'Invalid credentials'}, status=400)

        except Exception as e:
            print("Internal Server Error:", str(e))  
            return JsonResponse({'error': 'Internal Server Error: ' + str(e)}, status=500)

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)


