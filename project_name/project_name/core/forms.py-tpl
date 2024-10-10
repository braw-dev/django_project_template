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
