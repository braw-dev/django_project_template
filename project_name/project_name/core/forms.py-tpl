from django import forms

from . import models


class NewsletterSignupForm(forms.ModelForm):
    ALREADY_SUBSCRIBED_ERROR = "You are already subscribed."

    class Meta:
        model = models.NewsletterSignup
        fields = ("email",)
        widgets = {"email": forms.EmailInput(attrs={"data-testid": "newsletter-signup-form"})}

    def validate_unique(self) -> None:
        try:
            self.instance.validate_unique()
        except forms.ValidationError:
            self.add_error("email", self.ALREADY_SUBSCRIBED_ERROR)


class EmployerReviewMVPForm(forms.ModelForm):
    class Meta:
        model = models.EmployerReviewMVP
        fields = (
            "company_name",
            "company_domain",
            "job_title",
            "location",
            "estimated_review_date",
            "tenure_months",
            "current_employee",
            "payslip",
            "review_title",
            "review",
            "culture_rating",
        )
        widgets = {
            "estimated_review_date": forms.DateInput(attrs={"type": "date"}),
            "payslip": forms.FileInput(attrs={"accept": ".pdf"}),
        }
        labels = {
            "company_name": "Company Name",
            "company_domain": "Company Domain",
            "job_title": "Job Title",
            "location": "Location",
            "estimated_review_date": "Estimated Review Date",
            "tenure_months": "Tenure Months",
            "current_employee": "Current Employee",
            "payslip": "Payslip",
            "review_title": "Review Title",
            "review": "Review",
            "culture_rating": "Culture Rating",
        }
        help_texts = {
            "company_domain": "The domain of the company, e.g. 'example.com'",
            "estimated_review_date": "Approximately when is your review valid?",
            "tenure_months": "How long have/did you worked there?",
            "current_employee": "Are you currently employed there?",
            "payslip": "An optional payslip to prove your review and get a verified badge",
            "review_title": "A title for your review",
            "review": "The review itself",
            "culture_rating": "A rating from 1 to 5",
        }
        error_messages = {
            "company_domain": {
                "invalid": "Please enter a valid domain name.",
            },
            "estimated_review_date": {
                "invalid": "Please enter a valid date.",
            },
            "tenure_months": {
                "invalid": "Please enter a valid number.",
            },
            "culture_rating": {
                "invalid": "Please enter a valid number.",
            },
        }
