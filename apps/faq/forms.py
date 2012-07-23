# -*- coding: utf-8 -*-
from django import forms
from apps.faq.models import Question

class QuestionForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'placeholder':'E-mail'
            }
        ),
        required=True
    )
    question = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder':'Вопрос'
            }
        ),
        required=True
    )

    class Meta:
        model = Question
        fields = ('email', 'question',)