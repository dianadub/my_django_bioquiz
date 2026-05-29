from django import forms
from .models import Question

class CellQuizForm(forms.Form):
    """Форма для выбора ответа в викторине"""
    user_choice = forms.ChoiceField(
        choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')],
        widget=forms.RadioSelect,
        label="Твой вариант",
        error_messages={'required': 'Пожалуйста, выбери один из вариантов'}
    )

class NumberQuizForm(forms.Form):
    """Форма для теста по картинке с цифрами"""
    answer = forms.CharField(
        max_length=10,
        label="Введите номер органоида",
        widget=forms.TextInput(attrs={'placeholder': 'Например: 5', 'style': 'width: 100px; text-align: center;'}),
        error_messages={'required': 'Пожалуйста, введите номер'}
    )
