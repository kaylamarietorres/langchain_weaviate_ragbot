from django.shortcuts import render, get_object_or_404, redirect
from .models import Conversation, Interaction
from .forms import InteractionForm, ConversationForm
from django.contrib.auth.decorators import login_required

from services.chat_services import Chat


# Retrieves all conversations for the current user, ordered by start time, and renders them in conversations/index.html
@login_required
def index(request):
    conversations = Conversation.objects.filter(user=request.user).order_by('-start_time')
    return render(request, 'conversations/index.html', {'conversations': conversations})


# Handles the detail page for a specific conversation, retrieves the conversation and its interactions
@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
    interactions = Interaction.objects.filter(conversation=conversation)

    # This block handles POST requests, it validates the form, processes the interaction, gets response from chat service, saves the interaction and redirects to the same page
    if request.method == 'POST':
        form = InteractionForm(request.POST)
        if form.is_valid():
            interaction = form.save(commit=False)
            print(interaction.query)
            chat_history = list(interactions.values('query', 'response'))
            response = Chat.chat(interaction.query, chat_history)
            interaction.conversation = conversation
            interaction.response = response["text"]
            interaction.save()
            return redirect('conversation_detail', conversation_id=conversation.conversation_id)

    # For GET requests, it creates a new form and renders the detail page with the conversation, interactions, form, and all user conversations for the sidebar
    else:
        form = InteractionForm()
    return render(request, 'conversations/conversation_detail.html', {
        'conversation': conversation,
        'interactions': interactions,
        'form': form,
        'conversations': Conversation.objects.filter(user=request.user).order_by('-start_time')  # Include all conversations for the sidebar
    })


# Creates a new conversation. For POST requests it validates the form, saves the new conversation, and redirects to its detail page. For GET requests, it renders the new conversation page with a form and all user conversations for the sidebar
@login_required
def new_conversation(request):
    if request.method == 'POST':
        form = ConversationForm(request.POST)
        if form.is_valid():
            conversation = form.save(commit=False)
            conversation.user = request.user  # Assign the current user to the conversation
            conversation.save()
            return redirect('conversation_detail', conversation_id=conversation.conversation_id)
    else:
        form = ConversationForm()
    return render(request, 'conversations/new_conversation.html', {
        'form': form,
        'conversations': Conversation.objects.filter(user=request.user).order_by('-start_time')  # Include all conversations for the sidebar
    })
