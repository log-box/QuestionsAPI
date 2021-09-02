from rest_framework import serializers

from mainapp.models import Iterview, QuestionsForInterview, AnswerOption


class IterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Iterview
        fields = ('title', 'description', 'start_date', 'finish_date',)


class QuestionsForInterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionsForInterview
        fields = ('type', 'text',)


class QuestionChoiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ('index', 'text', 'type')


