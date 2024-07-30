from django import forms
from .models import Interaction, Conversation

class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ['query']
        widget = forms.Textarea(attrs={
                'class': 'custom-textarea',
                'id': "user-input",
                'placeholder': 'Type your message...'
            })

class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Conversation title'}),
        }
