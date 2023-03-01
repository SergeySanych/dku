# Generated by Django 4.1.4 on 2023-02-20 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0083_workflowcontenttype'),
        ('projects', '0002_alter_projectpage_options_projectpage_project_avtor_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectSearch',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'verbose_name': 'Страница поиска',
            },
            bases=('wagtailcore.page',),
        ),
    ]