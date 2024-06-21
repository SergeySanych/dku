# Generated by Django 4.1.13 on 2024-06-19 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='MinisiteList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minisite_name', models.CharField(max_length=50)),
                ('minisite_header_ru', models.CharField(blank=True, max_length=250, null=True)),
                ('minisite_header_en', models.CharField(blank=True, max_length=250, null=True)),
                ('minisite_subheader_ru', models.CharField(blank=True, max_length=250, null=True)),
                ('minisite_subheader_en', models.CharField(blank=True, max_length=250, null=True)),
                ('minisite_logo_list', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'verbose_name': 'Minisite list',
                'verbose_name_plural': 'Minisite list',
            },
        ),
    ]
