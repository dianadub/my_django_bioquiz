from django.db import models

class Question(models.Model):
    text = models.CharField(max_length=500)
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct = models.CharField(max_length=1)
    explanation = models.TextField(blank=True, verbose_name="Пояснение")

    def get_correct_display(self):
        return getattr(self, f'option_{self.correct}')

    def __str__(self):
        return self.text
