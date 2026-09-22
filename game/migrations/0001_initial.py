from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Word",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("word", models.CharField(max_length=5, unique=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "db_table": "game_word",
                "ordering": ["id"],
            },
        ),
    ]
