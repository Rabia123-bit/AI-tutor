from django.db import models


from django.db import models


class TutorLog(models.Model):
    student_name = models.CharField(max_length=100, blank=True, null=True)
    module = models.CharField(max_length=50)
    topic = models.CharField(max_length=100, blank=True, null=True)
    difficulty = models.CharField(max_length=50, blank=True, null=True)
    request_text = models.TextField(blank=True, null=True)
    response_text = models.TextField(blank=True, null=True)
    quiz_score = models.IntegerField(blank=True, null=True)
    total_questions = models.IntegerField(blank=True, null=True)
    response_time_ms = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, default="success")
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.module} | {self.topic} | {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


class TutorEvaluation(models.Model):
    MODULE_CHOICES = [
        ("theory", "Theory Module"),
        ("practical", "Practical Module"),
    ]

    evaluator_name = models.CharField(max_length=100)
    evaluated_module = models.CharField(max_length=20, choices=MODULE_CHOICES)
    q1_complete_explanations = models.IntegerField()
    q2_improves_understanding = models.IntegerField()
    q3_quiz_consistency = models.IntegerField()
    q4_response_reliability = models.IntegerField()
    q5_useful_for_learning = models.IntegerField()
    q6_increases_motivation = models.IntegerField()
    q7_overall_satisfaction = models.IntegerField()

    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def average_score(self):
        return round(
            (
                self.q1_complete_explanations +
                self.q2_improves_understanding +
                self.q3_quiz_consistency +
                self.q4_response_reliability +
                self.q5_useful_for_learning +
                self.q6_increases_motivation +
                self.q7_overall_satisfaction
            ) / 7,
            2
        )

    def __str__(self):
        return f"{self.evaluator_name} - {self.evaluated_module}"


