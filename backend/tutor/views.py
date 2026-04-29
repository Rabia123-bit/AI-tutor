import time
import logging
import csv
from django.http import HttpResponse 
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .services.theory_tutor import generate_theory_response
from .models import TutorLog
from .models import TutorEvaluation

logger = logging.getLogger("tutor")

import csv
from django.http import HttpResponse
from .models import TutorEvaluation


def export_evaluations_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="evaluation_results.csv"'

    writer = csv.writer(response)

    # Header row (adjust based on your model fields)
    writer.writerow([
        'Student Name',
        'Module',
        'Clarity',
        'Usefulness',
        'Engagement',
        'Overall Experience',
        'Comments',
        'Created At'
    ])

    evaluations = TutorEvaluation.objects.all().order_by('-created_at')

    for e in evaluations:
        writer.writerow([
            e.student_name,
            e.module,
            getattr(e, 'clarity', ''),
            getattr(e, 'usefulness', ''),
            getattr(e, 'engagement', ''),
            getattr(e, 'overall_experience', ''),
            getattr(e, 'comments', ''),
            e.created_at
        ])

    return response

def home(request):
    return render(request, "tutor/home.html")


def theory_page(request):
    return render(request, "tutor/theory.html")


def practical(request):
    return render(request, "tutor/practical.html")


@require_POST
def theory_tutor_view(request):
    start_time = time.time()

    topic = request.POST.get("topic", "").strip()
    difficulty = request.POST.get("difficulty", "Beginner").strip()

    logger.info(f"Theory request received | topic={topic} | difficulty={difficulty}")

    if not topic:
        logger.warning("Theory request failed: no topic selected")
        return JsonResponse({"error": "No topic selected."}, status=400)

    try:
        answer = generate_theory_response(topic, difficulty)
        response_time_ms = int((time.time() - start_time) * 1000)

        logger.info(
            f"Theory response generated | topic={topic} | difficulty={difficulty} | response_time_ms={response_time_ms}"
        )

        TutorLog.objects.create(
            module="theory",
            topic=topic,
            difficulty=difficulty,
            request_text=f"Topic: {topic}, Difficulty: {difficulty}",
            response_text=answer,
            response_time_ms=response_time_ms,
            status="success",
        )

        return JsonResponse({"answer": answer}, status=200)

    except Exception as e:
        response_time_ms = int((time.time() - start_time) * 1000)

        logger.error(
            f"Theory response failed | topic={topic} | difficulty={difficulty} | response_time_ms={response_time_ms} | error={str(e)}"
        )

        TutorLog.objects.create(
            module="theory",
            topic=topic,
            difficulty=difficulty,
            request_text=f"Topic: {topic}, Difficulty: {difficulty}",
            response_time_ms=response_time_ms,
            status="error",
            error_message=str(e),
        )

        return JsonResponse(
            {"error": "Tutor temporarily unavailable. Please try again."},
            status=500
        )
