# Generated by Django 3.1.2 on 2020-10-14 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid_app', '0006_agg_pcrtestssymptoms'),
    ]

    operations = [
        migrations.CreateModel(
            name='agg_Alltests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_date', models.DateField(blank=True, null=True)),
                ('total_tests', models.IntegerField(null=True)),
                ('total_pos', models.IntegerField(null=True)),
            ],
        ),
    ]
