from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tenancy", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="team",
            name="billing_country",
            field=models.CharField(
                blank=True,
                help_text="Two-letter billing country code used for VAT identity capture.",
                max_length=2,
                null=True,
                verbose_name="Billing country",
            ),
        ),
        migrations.AddField(
            model_name="team",
            name="vat_number",
            field=models.CharField(
                blank=True,
                help_text="Team VAT number without spaces. Validation is optional and service-driven.",
                max_length=32,
                null=True,
                verbose_name="VAT number",
            ),
        ),
        migrations.AddField(
            model_name="team",
            name="vat_validated_at",
            field=models.DateTimeField(
                blank=True,
                null=True,
                verbose_name="VAT validated at",
            ),
        ),
    ]
