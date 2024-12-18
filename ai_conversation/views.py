from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('conversation')
    return render(request, 'login.html')

@login_required
def conversation_view(request):
    return render(request, 'conversation.html')

@csrf_exempt
@login_required
def conversation_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')
        
        # Here you would process the user's message and generate an AI response
        # For now, we'll just echo the message back
        ai_response = f"You said: {user_message}"
        
        return JsonResponse({'response': ai_response})