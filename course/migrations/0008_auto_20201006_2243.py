# Generated by Django 3.1.1 on 2020-10-06 22:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_auto_20201006_1732'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='section',
            options={'ordering': ['lecture', 'name']},
        ),
    ]