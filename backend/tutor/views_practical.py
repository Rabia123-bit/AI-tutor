import time
import logging

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import TutorLog
from .services import retail_analytics as ra
from .services.practical_tutor import explain_practical_result

logger = logging.getLogger("tutor")


TOPIC_ACTIONS = {
    "Data Warehousing": {
        "warehouse_dimension_summary": "Warehouse Dimension Summary",
        "fact_table_summary": "Fact Table Summary",
    },
    "ETL": {
        "data_quality_summary": "Data Quality Summary",
        "etl_category_standardization_check": "Category Standardization Check",
    },
    "KPIs": {
        "total_revenue": "Total Revenue",
        "total_orders": "Total Orders",
        "average_order_value": "Average Order Value",
        "top_categories": "Top Categories by Revenue",
    },
    "SQL": {
        "sql_sales_by_category": "SQL: Sales by Category",
        "sql_top_stores": "SQL: Top Stores by Revenue",
        "sql_daily_revenue": "SQL: Daily Revenue Trend",
    },
    "Dashboards": {
        "dashboard_sales_overview": "Dashboard: Sales Overview",
        "dashboard_store_comparison": "Dashboard: Store Comparison",
        "dashboard_category_performance": "Dashboard: Category Performance",
    },
    "Predictive Analytics": {
        "daily_revenue_trend": "Daily Revenue Trend",
        "forecast_readiness_summary": "Forecast Readiness Summary",
    },
}


def practical_page(request):
    return render(request, "tutor/practical.html")


def _run_action(action: str):
    action_map = {
        "total_revenue": ra.total_revenue,
        "total_orders": ra.total_orders,
        "average_order_value": ra.average_order_value,
        "top_categories": ra.top_categories,
        "sql_sales_by_category": ra.sql_sales_by_category,
        "sql_top_stores": ra.sql_top_stores,
        "sql_daily_revenue": ra.sql_daily_revenue,
        "dashboard_sales_overview": ra.dashboard_sales_overview,
        "dashboard_store_comparison": ra.dashboard_store_comparison,
        "dashboard_category_performance": ra.dashboard_category_performance,
        "data_quality_summary": ra.data_quality_summary,
        "etl_category_standardization_check": ra.etl_category_standardization_check,
        "warehouse_dimension_summary": ra.warehouse_dimension_summary,
        "fact_table_summary": ra.fact_table_summary,
        "daily_revenue_trend": ra.daily_revenue_trend,
        "forecast_readiness_summary": ra.forecast_readiness_summary,
    }

    if action not in action_map:
        raise ValueError("Invalid analysis selected.")

    return action_map[action]()


@require_POST
def practical_api(request):
    start_time = time.time()

    topic = request.POST.get("topic", "").strip()
    difficulty = request.POST.get("difficulty", "Beginner").strip()
    action = request.POST.get("action", "").strip()
    question = request.POST.get("question", "").strip()

    if not topic:
        return JsonResponse({"error": "No topic selected."}, status=400)

    if topic not in TOPIC_ACTIONS:
        return JsonResponse({"error": "Invalid topic selected."}, status=400)

    if not action:
        return JsonResponse({"error": "No practical analysis selected."}, status=400)

    if action not in TOPIC_ACTIONS[topic]:
        return JsonResponse({"error": "Selected analysis does not belong to the chosen topic."}, status=400)

    if not question:
        question = "Interpret the result in business terms and explain its relevance to the selected BI topic."

    try:
        result = _run_action(action)
        action_label = TOPIC_ACTIONS[topic][action]

        explanation = explain_practical_result(
            student_question=question,
            result=result,
            topic=topic,
            difficulty=difficulty,
            action_label=action_label,
        )

        response_time_ms = int((time.time() - start_time) * 1000)

        logger.info(
            f"Practical success | topic={topic} | difficulty={difficulty} | action={action} | response_time_ms={response_time_ms}"
        )

        TutorLog.objects.create(
            module="practical",
            topic=topic,
            difficulty=difficulty,
            request_text=f"Action: {action_label} | Question: {question}",
            response_text=explanation,
            response_time_ms=response_time_ms,
            status="success",
        )

        return JsonResponse(
            {
                "result": result,
                "explanation": explanation,
                "action_label": action_label,
            },
            status=200,
        )

    except Exception as e:
        response_time_ms = int((time.time() - start_time) * 1000)

        logger.error(
            f"Practical failure | topic={topic} | difficulty={difficulty} | action={action} | error={str(e)}"
        )

        TutorLog.objects.create(
            module="practical",
            topic=topic,
            difficulty=difficulty,
            request_text=f"Action: {action} | Question: {question}",
            response_time_ms=response_time_ms,
            status="error",
            error_message=str(e),
        )

        return JsonResponse({"error": str(e)}, status=500)