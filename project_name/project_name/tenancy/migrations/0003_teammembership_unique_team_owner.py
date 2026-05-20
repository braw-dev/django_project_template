from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tenancy", "0002_team_vat_fields"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="teammembership",
            constraint=models.UniqueConstraint(
                fields=("team",),
                condition=models.Q(role="owner"),
                name="unique_team_owner",
            ),
        ),
    ]
