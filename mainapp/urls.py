from django.urls import path

from .views import AdminIterview, AdminQuestionsForInterview, AdminIterviewId

urlpatterns = [
    path('interviews/', AdminIterview.as_view()),
    path('interviews/<int:id>', AdminIterviewId.as_view()),
    path('interviews/<int:id>/quest/', AdminQuestionsForInterview.as_view()),

]
