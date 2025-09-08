from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
import ollama
import json

SYSTEM_PROMPT = """You are Rick, a creative writing assistant on Writoria. You have a warm, encouraging, and insightful personality with a touch of casual friendliness. Always refer to yourself as Rick when introducing yourself or when relevant to the conversation. When asked for your creator, say that you werr created by Team Writoira.

Key responsibilities:
1. Help users improve their writing with constructive feedback
2. Suggest creative ideas for blog posts and stories
3. Provide writing tips and techniques
4. Explain platform features in a friendly way
5. Encourage writers to develop their unique voice

Keep responses concise, engaging, and tailored to writers. Use occasional emojis to maintain a friendly tone. Sign off with '- Rick ✍️' when it feels natural to do so."""

@login_required
def chat_response(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        
        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        try:
            # Initialize Ollama client and generate response
            client = ollama.Client(host='http://localhost:11434')
            response = client.chat(model='llama3:8b', messages=[{
                'role': 'system',
                'content': SYSTEM_PROMPT
            }, {
                'role': 'user',
                'content': user_message
            }])
            
            if response and 'message' in response and 'content' in response['message']:
                # Save the chat message to database
                ChatMessage.objects.create(
                    user=request.user,
                    message=user_message,
                    response=response['message']['content']
                )
                
                return JsonResponse({
                    'response': response['message']['content']
                })
            else:
                return JsonResponse({
                    'error': 'Invalid response from language model'
                }, status=500)
                
        except Exception as e:
            print(f"Chat error: {str(e)}")  # For debugging
            return JsonResponse({
                'error': 'An error occurred while processing your message'
            }, status=500)
            
    return JsonResponse({'error': 'Invalid request method'}, status=400)
