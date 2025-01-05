import os
import shutil
import fileinput

def copy_module(src, dst):
    shutil.copytree(src, dst)

def modify_file(file_path, old_string, new_string):
    with fileinput.FileInput(file_path, inplace=True) as file:
        for line in file:
            print(line.replace(old_string, new_string), end='')

def main():
    # Copy ai_conversation to ai_codebot
    copy_module('ai_conversation', 'ai_codebot')

    # Modify apps.py
    modify_file('ai_codebot/apps.py', 'AiConversationConfig', 'AiCodebotConfig')
    modify_file('ai_codebot/apps.py', "'ai_conversation'", "'ai_codebot'")

    # Modify urls.py
    modify_file('ai_codebot/urls.py', 'from . import views', 'from . import views\nfrom django.urls import path, include')
    modify_file('ai_codebot/urls.py', "path('login/', views.login_view, name='login'),", "path('', views.login_view, name='codebot_login'),")
    modify_file('ai_codebot/urls.py', "path('conversation/', views.conversation_view, name='conversation'),", "path('conversation/', views.conversation_view, name='codebot_conversation'),")
    modify_file('ai_codebot/urls.py', "path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),", "path('logout/', auth_views.LogoutView.as_view(next_page='codebot_login'), name='codebot_logout'),")
    modify_file('ai_codebot/urls.py', "path('api/conversation/', views.conversation_api, name='conversation_api'),", "path('api/conversation/', views.conversation_api, name='codebot_conversation_api'),")

    # Modify views.py
    modify_file('ai_codebot/views.py', "return redirect('conversation')", "return redirect('codebot_conversation')")
    modify_file('ai_codebot/views.py', "return render(request, 'login.html')", "return render(request, 'codebot_login.html')")
    modify_file('ai_codebot/views.py', "return render(request, 'conversation.html')", "return render(request, 'codebot_conversation.html')")

    # Rename and modify templates
    os.rename('ai_codebot/templates/login.html', 'ai_codebot/templates/codebot_login.html')
    os.rename('ai_codebot/templates/conversation.html', 'ai_codebot/templates/codebot_conversation.html')
    modify_file('ai_codebot/templates/codebot_conversation.html', "{% url 'logout' %}", "{% url 'codebot_logout' %}")
    modify_file('ai_codebot/templates/codebot_conversation.html', "'/ai/api/conversation/'", "'/codebot/api/conversation/'")

    # Modify project's urls.py
    project_urls = 'django_ai/urls.py'  # Adjust this if your project has a different name
    with open(project_urls, 'r') as file:
        content = file.read()
    
    if "path('codebot/', include('ai_codebot.urls'))," not in content:
        with open(project_urls, 'w') as file:
            new_content = content.replace(
                "urlpatterns = [",
                "urlpatterns = [\n    path('codebot/', include('ai_codebot.urls')),"
            )
            file.write(new_content)

    # Modify project's settings.py
    project_settings = 'django_ai/settings.py'  # Adjust this if your project has a different name
    with open(project_settings, 'r') as file:
        content = file.read()
    
    if "'ai_codebot'," not in content:
        with open(project_settings, 'w') as file:
            new_content = content.replace(
                "'ai_conversation',",
                "'ai_conversation',\n    'ai_codebot',"
            )
            file.write(new_content)

    print("Modifications completed successfully!")

if __name__ == "__main__":
    main()