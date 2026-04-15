from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Avg

from .models import TutorEvaluation


def tutor_evaluation_dashboard(request):
    evaluations = TutorEvaluation.objects.order_by("-created_at")

    theory_evaluations = TutorEvaluation.objects.filter(evaluated_module="theory")
    practical_evaluations = TutorEvaluation.objects.filter(evaluated_module="practical")

    theory_avg = theory_evaluations.aggregate(
        q1=Avg("q1_complete_explanations"),
        q2=Avg("q2_improves_understanding"),
        q3=Avg("q3_quiz_consistency"),
        q4=Avg("q4_response_reliability"),
        q5=Avg("q5_useful_for_learning"),
        q6=Avg("q6_increases_motivation"),
        q7=Avg("q7_overall_satisfaction"),
    )

    practical_avg = practical_evaluations.aggregate(
        q1=Avg("q1_complete_explanations"),
        q2=Avg("q2_improves_understanding"),
        q3=Avg("q3_quiz_consistency"),
        q4=Avg("q4_response_reliability"),
        q5=Avg("q5_useful_for_learning"),
        q6=Avg("q6_increases_motivation"),
        q7=Avg("q7_overall_satisfaction"),
    )

    context = {
        "evaluations": evaluations,
        "theory_q1": round(theory_avg["q1"], 2) if theory_avg["q1"] is not None else 0,
        "theory_q2": round(theory_avg["q2"], 2) if theory_avg["q2"] is not None else 0,
        "theory_q3": round(theory_avg["q3"], 2) if theory_avg["q3"] is not None else 0,
        "theory_q4": round(theory_avg["q4"], 2) if theory_avg["q4"] is not None else 0,
        "theory_q5": round(theory_avg["q5"], 2) if theory_avg["q5"] is not None else 0,
        "theory_q6": round(theory_avg["q6"], 2) if theory_avg["q6"] is not None else 0,
        "theory_q7": round(theory_avg["q7"], 2) if theory_avg["q7"] is not None else 0,
        "practical_q1": round(practical_avg["q1"], 2) if practical_avg["q1"] is not None else 0,
        "practical_q2": round(practical_avg["q2"], 2) if practical_avg["q2"] is not None else 0,
        "practical_q3": round(practical_avg["q3"], 2) if practical_avg["q3"] is not None else 0,
        "practical_q4": round(practical_avg["q4"], 2) if practical_avg["q4"] is not None else 0,
        "practical_q5": round(practical_avg["q5"], 2) if practical_avg["q5"] is not None else 0,
        "practical_q6": round(practical_avg["q6"], 2) if practical_avg["q6"] is not None else 0,
        "practical_q7": round(practical_avg["q7"], 2) if practical_avg["q7"] is not None else 0,
    }

    return render(request, "tutor/evaluation_dashboard.html", context)


def tutor_evaluation_form(request):
    selected_module = request.GET.get("module", "").strip()
    evaluator_name = request.GET.get("student_name", "").strip()

    if selected_module not in ["theory", "practical"]:
        selected_module = ""

    return render(
        request,
        "tutor/evaluation_form.html",
        {
            "selected_module": selected_module,
            "evaluator_name": evaluator_name,
        }
    )

@require_POST
def save_tutor_evaluation(request):
    evaluator_name = request.POST.get("evaluator_name", "").strip()
    evaluated_module = request.POST.get("evaluated_module", "").strip()
    comments = request.POST.get("comments", "").strip()

    try:
        q1_complete_explanations = int(request.POST.get("q1_complete_explanations"))
        q2_improves_understanding = int(request.POST.get("q2_improves_understanding"))
        q3_quiz_consistency = int(request.POST.get("q3_quiz_consistency"))
        q4_response_reliability = int(request.POST.get("q4_response_reliability"))
        q5_useful_for_learning = int(request.POST.get("q5_useful_for_learning"))
        q6_increases_motivation = int(request.POST.get("q6_increases_motivation"))
        q7_overall_satisfaction = int(request.POST.get("q7_overall_satisfaction"))
    except (TypeError, ValueError):
        return JsonResponse({"error": "All evaluation fields must be valid integers."}, status=400)

    if not evaluator_name:
        return JsonResponse({"error": "Evaluator name is required."}, status=400)

    if evaluated_module not in ["theory", "practical"]:
        return JsonResponse({"error": "Please select either Theory Module or Practical Module."}, status=400)

    valid_scores = {1, 2, 3, 4, 5}
    values = [
        q1_complete_explanations,
        q2_improves_understanding,
        q3_quiz_consistency,
        q4_response_reliability,
        q5_useful_for_learning,
        q6_increases_motivation,
        q7_overall_satisfaction,
    ]

    if not all(v in valid_scores for v in values):
        return JsonResponse({"error": "All scores must be between 1 and 5."}, status=400)

    TutorEvaluation.objects.create(
        evaluator_name=evaluator_name,
        evaluated_module=evaluated_module,
        q1_complete_explanations=q1_complete_explanations,
        q2_improves_understanding=q2_improves_understanding,
        q3_quiz_consistency=q3_quiz_consistency,
        q4_response_reliability=q4_response_reliability,
        q5_useful_for_learning=q5_useful_for_learning,
        q6_increases_motivation=q6_increases_motivation,
        q7_overall_satisfaction=q7_overall_satisfaction,
        comments=comments if comments else None,
    )

    return JsonResponse({"message": "Tutor evaluation saved successfully."}, status=200)