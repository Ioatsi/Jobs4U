# Generated by Django 3.2.3 on 2022-05-26 21:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('JobScraper', '0002_alter_joblisting_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joblisting',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
