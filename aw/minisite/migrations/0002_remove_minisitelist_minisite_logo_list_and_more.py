# Generated by Django 4.1.13 on 2024-06-19 13:16

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('minisite', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='minisitelist',
            name='minisite_logo_list',
        ),
        migrations.CreateModel(
            name='MiniSiteGalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('minisite_key', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='minisite_gallery_images', to='minisite.minisitelist')),
                ('minisite_logo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
