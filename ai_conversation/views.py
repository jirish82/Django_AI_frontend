from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from ai_services.ai_query import query_ai_sync

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
        file_paths = data.get('file_paths')
        
        # Query the AI using the new functionality
        ai_response = query_ai_sync(user_message, file_paths, online_search=True)
        
        return JsonResponse({'response': ai_response})
    
    # Handle GET requests or other methods
    return JsonResponse({'error': 'Invalid request method'}, status=405)