import uuid
import json
import logging
import time

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .services.quiz_tutor import generate_quiz
from .models import TutorLog

logger = logging.getLogger("tutor")


@require_POST
def theory_quiz_api(request):
    start_time = time.time()

    topic = request.POST.get("topic", "").strip()
    difficulty = request.POST.get("difficulty", "Beginner").strip()
    context_text = request.POST.get("context_text", "").strip()

    if not topic:
        return JsonResponse({"error": "No topic provided."}, status=400)

    try:
        quiz = generate_quiz(
            topic=topic,
            difficulty=difficulty,
            student_text=context_text or None
        )

        quiz_id = str(uuid.uuid4())

        correct_answers = []
        safe_questions = []

        for q in quiz["questions"]:
            options = q["options"]
            answer_index = q["answer_index"]

            # store full grading data in session
            correct_answers.append({
                "question_text": q["q"],
                "options": options,
                "answer_index": answer_index,
                "correct_answer_text": options[answer_index],
                "explanation": q["explanation"],
            })

            # send safe data to frontend
            safe_questions.append({
                "q": q["q"],
                "options": options,
            })

        request.session[f"quiz_{quiz_id}"] = correct_answers
        request.session.modified = True

        response_time_ms = int((time.time() - start_time) * 1000)

        logger.info(
            f"Quiz generated | topic={topic} | difficulty={difficulty} | response_time_ms={response_time_ms}"
        )

        TutorLog.objects.create(
            module="quiz_generation",
            topic=topic,
            difficulty=difficulty,
            request_text=context_text if context_text else f"Quiz requested for {topic}",
            response_text=json.dumps(safe_questions),
            response_time_ms=response_time_ms,
            total_questions=len(safe_questions),
            status="success",
        )

        return JsonResponse({
            "quiz_id": quiz_id,
            "topic": quiz.get("topic", topic),
            "difficulty": quiz.get("difficulty", difficulty),
            "questions": safe_questions,
        })

    except Exception as e:
        response_time_ms = int((time.time() - start_time) * 1000)

        logger.error(
            f"Quiz generation failed | topic={topic} | difficulty={difficulty} | error={str(e)}"
        )

        TutorLog.objects.create(
            module="quiz_generation",
            topic=topic,
            difficulty=difficulty,
            request_text=context_text if context_text else f"Quiz requested for {topic}",
            response_time_ms=response_time_ms,
            status="error",
            error_message=str(e),
        )

        return JsonResponse({"error": f"Quiz generation failed: {str(e)}"}, status=500)


@require_POST
def grade_quiz_api(request):
    start_time = time.time()

    quiz_id = request.POST.get("quiz_id", "").strip()
    answers_raw = request.POST.get("answers", "").strip()
    topic = request.POST.get("topic", "").strip()
    difficulty = request.POST.get("difficulty", "").strip()

    if not quiz_id:
        return JsonResponse({"error": "Missing quiz_id."}, status=400)

    if not answers_raw:
        return JsonResponse({"error": "Missing answers."}, status=400)

    session_key = f"quiz_{quiz_id}"
    correct_answers = request.session.get(session_key)

    if not correct_answers:
        return JsonResponse({"error": "Quiz not found or expired. Please generate it again."}, status=400)

    try:
        answers = json.loads(answers_raw)

        if not isinstance(answers, list):
            return JsonResponse({"error": "Answers must be a list."}, status=400)

        score = 0
        details = []

        for i, correct in enumerate(correct_answers):
            options = correct["options"]
            user_answer_index = answers[i] if i < len(answers) else None
            correct_answer_index = correct["answer_index"]

            is_correct = user_answer_index == correct_answer_index
            if is_correct:
                score += 1

            user_answer_text = None
            if isinstance(user_answer_index, int) and 0 <= user_answer_index < len(options):
                user_answer_text = options[user_answer_index]

            correct_answer_text = correct["correct_answer_text"]
            explanation = correct["explanation"]

            if user_answer_index is None:
                wrong_reason = "No option was selected for this question."
            elif is_correct:
                wrong_reason = "Your selected answer matches the correct BI concept."
            else:
                wrong_reason = (
                    f'Your selected answer ("{user_answer_text}") does not match the correct concept. '
                    f'The correct answer is "{correct_answer_text}".'
                )

            review_note = (
                f"Review the concept related to: {correct['question_text']}"
                if not is_correct else
                "Good job. You understood this concept correctly."
            )

            details.append({
                "question_number": i + 1,
                "question_text": correct["question_text"],
                "your_answer_index": user_answer_index,
                "your_answer_text": user_answer_text,
                "correct_answer_index": correct_answer_index,
                "correct_answer_text": correct_answer_text,
                "correct": is_correct,
                "why_correct": explanation,
                "why_your_answer_wrong": wrong_reason,
                "review_note": review_note,
            })

        response_time_ms = int((time.time() - start_time) * 1000)

        logger.info(
            f"Quiz graded | topic={topic} | difficulty={difficulty} | score={score}/{len(correct_answers)}"
        )

        TutorLog.objects.create(
            module="quiz_result",
            topic=topic if topic else None,
            difficulty=difficulty if difficulty else None,
            request_text=answers_raw,
            response_text=json.dumps(details),
            quiz_score=score,
            total_questions=len(correct_answers),
            response_time_ms=response_time_ms,
            status="success",
        )

        return JsonResponse({
            "score": score,
            "total": len(correct_answers),
            "details": details,
        })

    except Exception as e:
        response_time_ms = int((time.time() - start_time) * 1000)

        logger.error(f"Quiz grading failed | error={str(e)}")

        TutorLog.objects.create(
            module="quiz_result",
            topic=topic if topic else None,
            difficulty=difficulty if difficulty else None,
            request_text=answers_raw,
            response_time_ms=response_time_ms,
            status="error",
            error_message=str(e),
        )

        return JsonResponse({"error": f"Grading failed: {str(e)}"}, status=500)