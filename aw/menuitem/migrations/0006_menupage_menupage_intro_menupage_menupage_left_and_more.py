# Generated by Django 4.1.4 on 2023-02-16 05:19

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0024_index_image_file_hash'),
        ('menuitem', '0005_remove_menupage_menupage_workcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='menupage',
            name='menupage_intro',
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='menupage',
            name='menupage_left',
            field=models.BooleanField(default=False, verbose_name='Показывать слева'),
        ),
        migrations.AddField(
            model_name='menupage',
            name='menupage_vitrina',
            field=models.BooleanField(default=False, verbose_name='Показывать витрину'),
        ),
        migrations.CreateModel(
            name='MenuPageGalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('menupage_image_caption', models.CharField(blank=True, max_length=250)),
                ('menupage_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailimages.image')),
                ('menupage_key', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='menupage_gallery_images', to='menuitem.menupage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
