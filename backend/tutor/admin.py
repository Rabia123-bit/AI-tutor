from django.contrib import admin
from .models import TutorLog, TutorEvaluation


@admin.register(TutorLog)
class TutorLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "module",
        "topic",
        "difficulty",
        "quiz_score",
        "total_questions",
        "response_time_ms",
        "status",
        "created_at",
    )
    list_filter = ("module", "topic", "difficulty", "status", "created_at")
    search_fields = ("topic", "request_text", "response_text", "error_message")



@admin.register(TutorEvaluation)
class TutorEvaluationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "evaluator_name",
        "evaluated_module",
        "q1_complete_explanations",
        "q2_improves_understanding",
        "q3_quiz_consistency",
        "q4_response_reliability",
        "q5_useful_for_learning",
        "q6_increases_motivation",
        "q7_overall_satisfaction",
        "created_at",
    )
    list_filter = ("evaluated_module", "created_at")
    search_fields = ("evaluator_name", "comments")