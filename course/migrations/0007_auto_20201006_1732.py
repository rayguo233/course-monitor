# Generated by Django 3.1.1 on 2020-10-06 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_auto_20201001_1536'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['abbrev']},
        ),
        migrations.AlterModelOptions(
            name='lecture',
            options={'ordering': ['course', 'name']},
        ),
    ]
