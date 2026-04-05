# pylint: disable=missing-module-docstring,missing-final-newline
# Маршруты викторины
from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('theory/', views.theory_page, name='theory'),
    path('diagram/', views.cell_diagram, name='cell_diagram'),
    path('q/<int:q_id>/', views.show_question, name='show_question'),
    path('next/<int:q_id>/', views.go_to_next_question, name='next_question'),
    path('final/', views.summary_page, name='summary_page'),
    path('numbered-quiz/', views.numbered_quiz, name='numbered_quiz'),
    path('reset-numbered/', views.reset_numbered_quiz, name='reset_numbered_quiz'),
    path('stats/', views.user_stats, name='user_stats'),
]
