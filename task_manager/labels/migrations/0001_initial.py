from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Label",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150, unique=True, verbose_name="Name")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Created at")),
            ],
            options={
                "ordering": ("pk",),
                "verbose_name": "Label",
                "verbose_name_plural": "Labels",
            },
        ),
    ]
