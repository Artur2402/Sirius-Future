# Generated by Django 5.1.1 on 2024-09-05 13:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referrals', '0003_student_lessons_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='lessons_count',
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=4)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('referrer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='referrer_lessons', to='referrals.user')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='referrals.student')),
            ],
        ),
    ]
