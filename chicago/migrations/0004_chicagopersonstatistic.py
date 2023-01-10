# Generated by Django 3.2.16 on 2023-01-09 03:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chicago', '0003_chicagoorganization_chicagoperson'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChicagoPersonStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_list', models.JSONField(null=True)),
                ('attendance_percent', models.CharField(max_length=10)),
                ('legislation_count', models.IntegerField()),
                ('person', models.OneToOneField(help_text='A link to the Person connected to this statistic record.', on_delete=django.db.models.deletion.CASCADE, related_name='statistics', to='chicago.chicagoperson')),
            ],
        ),
    ]
