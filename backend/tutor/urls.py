from django.urls import path
from . import views
from .views_quiz import theory_quiz_api, grade_quiz_api
from .views_practical import practical_api
from .views_logs import logs_dashboard
from .views_evaluation import tutor_evaluation_form, tutor_evaluation_dashboard, save_tutor_evaluation
from .views import export_evaluations_csv

urlpatterns = [
    path("", views.home, name="home"),
    path("theory/", views.theory_page, name="theory"),
    path("api/theory-tutor/", views.theory_tutor_view, name="theory_tutor"),
    path("api/theory-quiz/", theory_quiz_api, name="theory_quiz"),
    path("api/grade-quiz/", grade_quiz_api, name="grade_quiz"),
    path("practical/", views.practical, name="practical"),
    path("api/practical/", practical_api, name="practical_api"),
    path("logs/", logs_dashboard, name="logs_dashboard"),
    path("export-evaluations/", export_evaluations_csv, name="export_evaluations_csv"),
    path("evaluation/", tutor_evaluation_dashboard, name="tutor_evaluation_dashboard"),
    path("evaluation/form/", tutor_evaluation_form, name="tutor_evaluation_form"),
    path("api/save-evaluation/", save_tutor_evaluation, name="save_tutor_evaluation"),

]
