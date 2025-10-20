from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("labels", "0001_initial"),
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="labels",
            field=models.ManyToManyField(blank=True, related_name="tasks", to="labels.label", verbose_name="Labels"),
        ),
    ]
