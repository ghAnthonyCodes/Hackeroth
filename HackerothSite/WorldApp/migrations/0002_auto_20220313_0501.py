# Generated by Django 3.2.12 on 2022-03-13 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WorldApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commit',
            name='additions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='commit',
            name='deletions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='commit',
            name='total',
            field=models.IntegerField(default=0),
        ),
    ]
