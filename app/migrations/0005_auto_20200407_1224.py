# Generated by Django 3.0.4 on 2020-04-07 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_a'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.TextField(default=1),
        ),
        migrations.DeleteModel(
            name='A',
        ),
    ]
