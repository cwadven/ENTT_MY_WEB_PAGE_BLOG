# Generated by Django 2.2.6 on 2019-10-08 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_board_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='Body',
            field=models.TextField(),
        ),
    ]
