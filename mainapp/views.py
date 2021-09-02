from datetime import date

from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework import authentication, permissions
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView

from mainapp.models import Iterview, AnswerOption, QuestionsForInterview
from mainapp.serializers import IterviewSerializer, QuestionsForInterviewSerializer, QuestionChoiseSerializer


class AdminAPIView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]


class AdminIterview(AdminAPIView):
    def get(self, request):
        return Response(IterviewSerializer(Iterview.objects.all(), many=True).data)

    def post(self, request):
        try:
            serializer = IterviewSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            newIterview = Iterview(**data)
            newIterview.save()
            return Response(IterviewSerializer(newIterview).data)
        except Exception as ex:
            raise ParseError(ex)


class AdminIterviewId(AdminAPIView):
    def get(self, request, id):
        try:
            interviews = Iterview.objects.get(id=id)
            result = IterviewSerializer(interviews).data
            result['questions'] = []
            for question in interviews.questionsforinterview_set.all():
                questDict = QuestionsForInterviewSerializer(question).data
                if question.hasChoise:
                    questDict['options'] = QuestionChoiseSerializer(question.option_set.all(), many=True).data
                result['questions'].append(questDict)

            return Response(result)

        except interviews.DoesNotExist:
            raise Http404()
        except Exception as e:
            raise ParseError(e)

    def delete(self, request, id):
        try:
            Iterview.objects.get(id=id).delete()
            return Response('Deleted')
        except Iterview.DoesNotExist:
            raise Http404()
        except Exception as ex:
            raise ParseError(ex)

    def patch(self, request, id):
        try:
            interviews = Iterview.objects.get(id=id)
            data = request.data
            if 'title' in data:
                interviews.title = data['title']
            if 'description' in data:
                interviews.description = data['description']
            if 'finish_date' in data:
                interviews.finish_date = date.fromisoformat(data['finish_date'])

            interviews.save()
            return Response(IterviewSerializer(interviews).data)

        except Iterview.DoesNotExist:
            raise Http404()
        except Exception as ex:
            raise ParseError(ex)


class AdminQuestionsForInterview(AdminAPIView):
    # добавляем вопросы к интервью
    def post(self, request, id):
        try:
            interview = Iterview.objects.get(id=id)
            result = QuestionsForInterviewSerializer(data=request.data)  # получили вопрос
            result.is_valid(raise_exception=True)
            result_dict = dict(result.validated_data)
            result_dict['interview'] = interview  # получили интервью
            addingQuestion = QuestionsForInterview(**result_dict)
            answerChoises = addingQuestion.hasChoise
            choiseList = []
            if answerChoises:
                if not 'choises' in request.data:  # в JSON вопросы должны лежать по ключу choises
                    raise Exception('забыли варианты')
                if type(request.data['choises']) != list or len(request.data['choises']) < 2:  # вопросы должны быть списком
                    raise Exception('не правильно заданы опции вопроса')

                index = 1  # отсчет вариантов
                for choiseText in request.data['choises']:
                    choiseList.append(AnswerOption(
                        text=choiseText,
                        index=index
                    ))
                    index += 1

            addingQuestion.save()  # сохраняем сам вопрос
            if answerChoises:  # проверяем дополнительные опции вопроса и сохраняем их если есть
                for choise in choiseList:
                    choise.question = addingQuestion
                    choise.save()

            return Response(result.data)

        except Iterview.DoesNotExist:
            raise Http404()
        except Exception as ex:
            raise ParseError(ex)


class AdminQuestionId(AdminAPIView):
    # TODO
    pass

class AllIterview(APIView):
    # TODO
    pass

class IterviewId(APIView):
    # TODO
    pass

class UserIterviewId(APIView):
    # TODO
    pass

