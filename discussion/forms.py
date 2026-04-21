from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Question, Answer, Group, Poll
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'role')
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your doubt...'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your doubt in detail...', 'rows': 5}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your answer...', 'rows': 3}),
        }

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'category', 'can_post', 'can_comment', 'max_members', 'tags', 'icon', 'rules', 'discussion_format']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. AI Learners Hub'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Programming, AI/ML, Cloud'}),
            'can_post': forms.Select(attrs={'class': 'form-control'}),
            'can_comment': forms.Select(attrs={'class': 'form-control'}),
            'max_members': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Leave blank for unlimited'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Java, Python, Interview Prep'}),
            'icon': forms.FileInput(attrs={'class': 'form-control', 'style': 'padding: 10px;'}),
            'rules': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'No spam. Respect others. Stay on topic.'}),
            'discussion_format': forms.Select(attrs={'class': 'form-control'}),
        }

class PollCreationForm(forms.ModelForm):
    options = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter each poll option on a new line...'}),
        help_text="One option per line"
    )

    class Meta:
        model = Poll
        fields = ['question_text']
        widgets = {
            'question_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your poll question...'}),
        }
        
    def clean_options(self):
        data = self.cleaned_data['options']
        lines = [line.strip() for line in data.split('\n') if line.strip()]
        if len(lines) < 2:
            raise ValidationError("You must provide at least two options for a poll.")
        if len(lines) > 10:
            raise ValidationError("You can provide a maximum of 10 options.")
        return lines
