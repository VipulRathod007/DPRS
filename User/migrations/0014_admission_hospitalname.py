# Generated by Django 3.1.1 on 2021-03-29 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0013_admission_billamt'),
    ]

    operations = [
        migrations.AddField(
            model_name='admission',
            name='hospitalname',
            field=models.CharField(default='', max_length=150),
        ),
    ]
