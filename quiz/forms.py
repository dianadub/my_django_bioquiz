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

class NewQuestionForm(forms.ModelForm):
    """Форма для добавления нового вопроса пользователем"""
    class Meta:
        model = Question
        fields = ['text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct', 'explanation']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2}),
            'explanation': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'text': 'Текст вопроса',
            'option_a': 'Вариант A',
            'option_b': 'Вариант B',
            'option_c': 'Вариант C',
            'option_d': 'Вариант D',
            'correct': 'Правильный ответ (a/b/c/d)',
            'explanation': 'Пояснение',
        }

class NumberQuizForm(forms.Form):
    """Форма для теста по картинке с цифрами"""
    answer = forms.CharField(
        max_length=10,
        label="Введите номер органоида",
        widget=forms.TextInput(attrs={'placeholder': 'Например: 5', 'style': 'width: 100px; text-align: center;'}),
        error_messages={'required': 'Пожалуйста, введите номер'}
    )
