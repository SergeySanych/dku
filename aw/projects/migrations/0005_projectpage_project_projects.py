# Generated by Django 4.1.4 on 2023-02-28 13:20

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_projectpage_project_body_bottom_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectpage',
            name='project_projects',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='projects.projectpage'),
        ),
    ]
