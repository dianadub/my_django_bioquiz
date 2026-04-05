# pylint: disable=no-member,line-too-long,missing-function-docstring,missing-module-docstring,unused-argument
# Викторина по биологии "Клетка"
# Автор: [Твоё имя]

from django.shortcuts import render, redirect, get_object_or_404
from .models import Question
from .forms import CellQuizForm, NewQuestionForm, NumberQuizForm


def home_page(request):
    return render(request, 'home.html')


def theory_page(request):
    return render(request, 'theory.html')


def cell_diagram(request):
    return render(request, 'cell_diagram.html')


def show_question(request, q_id=1):
    total_questions = Question.objects.count()
    if total_questions == 0:
        return render(request, 'cell_question.html', {'error': 'Нет вопросов'})

    if q_id > total_questions:
        return redirect('summary_page')

    current_q = get_object_or_404(Question, id=q_id)

    already_answered = request.session.get(f'answered_{q_id}', False)
    is_correct_flag = request.session.get(f'is_correct_{q_id}', None)
    correct_answer_text = getattr(current_q, f'option_{current_q.correct}') if already_answered else None

    if request.method == 'POST':
        form = CellQuizForm(request.POST)
        if form.is_valid():
            user_answer = form.cleaned_data['user_choice']
            correct_letter = current_q.correct
            correct = (user_answer == correct_letter)
            request.session[f'answered_{q_id}'] = True
            request.session[f'is_correct_{q_id}'] = correct
            total_score = 0
            for i in range(1, total_questions + 1):
                if request.session.get(f'is_correct_{i}'):
                    total_score += 1
            request.session['total_score'] = total_score
            return redirect('show_question', q_id=q_id)
    else:
        form = CellQuizForm()

    current_score = 0
    for i in range(1, total_questions + 1):
        if request.session.get(f'is_correct_{i}'):
            current_score += 1

    context = {
        'question': current_q,
        'form': form,
        'current_num': q_id,
        'total_num': total_questions,
        'score': current_score,
        'answered': already_answered,
        'is_correct': is_correct_flag,
        'correct_text': correct_answer_text,
    }
    return render(request, 'cell_question.html', context)


def go_to_next_question(request, q_id):
    next_id = q_id + 1
    total_questions = Question.objects.count()
    if next_id > total_questions:
        return redirect('summary_page')
    return redirect('show_question', q_id=next_id)


def summary_page(request):
    total_questions = Question.objects.count()
    user_score = 0
    for i in range(1, total_questions + 1):
        if request.session.get(f'is_correct_{i}'):
            user_score += 1
    request.session.flush()
    return render(request, 'summary.html', {'score': user_score, 'total': total_questions})


def add_question(request):
    if request.method == 'POST':
        form = NewQuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('question_list')
    else:
        form = NewQuestionForm()
    return render(request, 'add_question.html', {'form': form})


def numbered_quiz(request):
    questions = [
        {'name': 'Ядро', 'correct': '6'},
        {'name': 'Аппарат Гольджи', 'correct': '3'},
        {'name': 'Центриоль', 'correct': '7'},
    ]

    current_index = request.session.get('numbered_index', 0)
    score = request.session.get('numbered_score', 0)

    if current_index >= len(questions):
        result = f"Твой результат: {score} из {len(questions)}"
        request.session['numbered_index'] = 0
        request.session['numbered_score'] = 0
        return render(request, 'numbered_quiz.html', {
            'result': result,
            'finished': True,
            'score': score,
            'total': len(questions)
        })

    current_q = questions[current_index]
    message = ''

    if request.method == 'POST':
        form = NumberQuizForm(request.POST)
        if form.is_valid():
            user_answer = form.cleaned_data['answer'].strip()
            if user_answer == current_q['correct']:
                score += 1
                request.session['numbered_score'] = score
                message = f"Правильно! {current_q['name']} обозначен цифрой {current_q['correct']}"
            else:
                message = f"Неправильно. {current_q['name']} обозначен цифрой {current_q['correct']}"
            request.session['numbered_index'] = current_index + 1
            return redirect('numbered_quiz')
    else:
        form = NumberQuizForm()

    context = {
        'form': form,
        'question': current_q,
        'current': current_index + 1,
        'total': len(questions),
        'score': score,
        'message': message,
    }
    return render(request, 'numbered_quiz.html', context)


def reset_numbered_quiz(request):
    request.session['numbered_index'] = 0
    request.session['numbered_score'] = 0
    return redirect('numbered_quiz')


def user_stats(request):
    total_questions = Question.objects.count()
    correct_count = 0
    for i in range(1, total_questions + 1):
        if request.session.get(f'is_correct_{i}'):
            correct_count += 1
    percent = round(correct_count / total_questions * 100, 1) if total_questions > 0 else 0
    context = {
        'total_questions': total_questions,
        'correct_count': correct_count,
        'percent': percent,
    }
    return render(request, 'stats.html', context)
