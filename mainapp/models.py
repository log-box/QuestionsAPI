from django.core.exceptions import ValidationError
from django.db import models


OPTION_TYPES = ['CHOICE', 'MULTIPLE_CHOICE']


class Iterview(models.Model):
    title = models.CharField(
        verbose_name='название',
        max_length=128,
    )
    description = models.CharField(
        verbose_name='описание',
        max_length=500,
    )
    start_date = models.DateField(
        auto_now_add=True,
    )
    finish_date = models.DateField(
        auto_now=True,
    )
    is_finish = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


class QuestionsForInterview(models.Model):
    interview = models.ForeignKey(
        Iterview,
        on_delete=models.CASCADE,
        primary_key=True
    )
    type = models.CharField(
        max_length=30,
    )
    text = models.CharField(max_length=500)

    @property
    def hasChoise(self):
        return self.type in OPTION_TYPES


class AnswerOption(models.Model):

    question = models.ForeignKey(
        QuestionsForInterview,
        on_delete=models.CASCADE,
    )
    index = models.PositiveIntegerField()  # счетчик вариантов
    text = models.CharField(max_length=100)


class InterviewDone(models.Model):
    # Пройденный опрос
    user = models.IntegerField(db_index=True)
    iterview = models.ForeignKey(Iterview, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)


class UserAnswer(models.Model):
    # ответ пользователя
    interviewDone = models.ForeignKey(InterviewDone, on_delete=models.CASCADE)
    questionsForInterview = models.ForeignKey(QuestionsForInterview, on_delete=models.CASCADE)
    questionType = models.CharField(max_length=15)
    questionText = models.CharField(max_length=500)
    answerText = models.CharField(max_length=500)
