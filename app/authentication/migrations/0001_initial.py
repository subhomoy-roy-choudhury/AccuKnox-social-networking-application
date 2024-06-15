# Generated by Django 5.0.6 on 2024-06-15 02:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="AuthUser",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        max_length=150,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Username must contain only letters, numbers, or underscores",
                                regex="^\\w+$",
                            )
                        ],
                    ),
                ),
                (
                    "email",
                    models.EmailField(db_index=True, max_length=254, unique=True),
                ),
                (
                    "firstname",
                    models.CharField(
                        max_length=150,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Firstname must contain only letters",
                                regex="^[a-zA-Z]+$",
                            )
                        ],
                    ),
                ),
                (
                    "lastname",
                    models.CharField(
                        max_length=150,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Lastname must contain only letters",
                                regex="^[a-zA-Z]+$",
                            )
                        ],
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="authuser",
            constraint=models.CheckConstraint(
                check=models.Q(("firstname__iregex", "^[a-zA-Z]+$")),
                name="firstname_valid",
            ),
        ),
        migrations.AddConstraint(
            model_name="authuser",
            constraint=models.CheckConstraint(
                check=models.Q(("lastname__iregex", "^[a-zA-Z]+$")),
                name="lastname_valid",
            ),
        ),
    ]