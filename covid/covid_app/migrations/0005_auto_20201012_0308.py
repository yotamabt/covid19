# Generated by Django 3.1.2 on 2020-10-12 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid_app', '0004_covid19apidata_deaths_no_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='covid19apidata',
            name='Confirmed',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='covid19apidata',
            name='daily_Confirmed',
            field=models.IntegerField(null=True),
        ),
    ]