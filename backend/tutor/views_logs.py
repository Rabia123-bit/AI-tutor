from django.shortcuts import render
from django.db.models import Count, Avg

from .models import TutorLog


def logs_dashboard(request):
    # Main grouped logs
    theory_logs = TutorLog.objects.filter(module="theory").order_by("-created_at")[:50]
    practical_logs = TutorLog.objects.filter(module="practical").order_by("-created_at")[:50]
    quiz_generation_logs = TutorLog.objects.filter(module="quiz_generation").order_by("-created_at")[:50]
    quiz_result_logs = TutorLog.objects.filter(module="quiz_result").order_by("-created_at")[:50]

    # Summary metrics
    total_theory = TutorLog.objects.filter(module="theory").count()
    total_practical = TutorLog.objects.filter(module="practical").count()
    total_quiz_generated = TutorLog.objects.filter(module="quiz_generation").count()
    total_quiz_results = TutorLog.objects.filter(module="quiz_result").count()

    avg_theory_response = TutorLog.objects.filter(
        module="theory",
        status="success"
    ).aggregate(avg=Avg("response_time_ms"))["avg"]

    avg_practical_response = TutorLog.objects.filter(
        module="practical",
        status="success"
    ).aggregate(avg=Avg("response_time_ms"))["avg"]

    avg_quiz_score = TutorLog.objects.filter(
        module="quiz_result",
        status="success"
    ).aggregate(avg=Avg("quiz_score"))["avg"]

    error_count = TutorLog.objects.filter(status="error").count()

    # Topic usage summary
    topic_summary = (
        TutorLog.objects.filter(module__in=["theory", "practical"])
        .exclude(topic__isnull=True)
        .exclude(topic__exact="")
        .values("topic")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    context = {
        "theory_logs": theory_logs,
        "practical_logs": practical_logs,
        "quiz_generation_logs": quiz_generation_logs,
        "quiz_result_logs": quiz_result_logs,
        "total_theory": total_theory,
        "total_practical": total_practical,
        "total_quiz_generated": total_quiz_generated,
        "total_quiz_results": total_quiz_results,
        "avg_theory_response": round(avg_theory_response, 2) if avg_theory_response else 0,
        "avg_practical_response": round(avg_practical_response, 2) if avg_practical_response else 0,
        "avg_quiz_score": round(avg_quiz_score, 2) if avg_quiz_score else 0,
        "error_count": error_count,
        "topic_summary": topic_summary,
    }
    return render(request, "tutor/logs_dashboard.html", context)