# Generated by Django 3.1.1 on 2020-10-01 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_auto_20201001_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='num_spots_taken',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='status',
            field=models.CharField(max_length=50, null=True),
        ),
    ]