# Generated by Django 4.1.4 on 2023-02-18 10:44

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('menuitem', '0010_alter_menupage_menupage_body'),
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('peoples', '0004_peoplesresearcherpage'),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectpage',
            options={'verbose_name': 'Страница проекта', 'verbose_name_plural': 'Страницы проектов'},
        ),
        migrations.AddField(
            model_name='projectpage',
            name='project_avtor',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='peoples.peoplespage'),
        ),
        migrations.AddField(
            model_name='projectpage',
            name='project_body',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='subtitle')), ('paragraph', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('leftheader', wagtail.blocks.StructBlock([('left', wagtail.blocks.CharBlock()), ('right', wagtail.blocks.RichTextBlock())])), ('imageleft', wagtail.blocks.StructBlock([('imgleft', wagtail.images.blocks.ImageChooserBlock()), ('txtright', wagtail.blocks.RichTextBlock())])), ('htmlcode', wagtail.blocks.RawHTMLBlock())], blank=True, use_json_field=True),
        ),
        migrations.AddField(
            model_name='projectpage',
            name='project_header',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='projectpage',
            name='project_left',
            field=models.BooleanField(default=False, verbose_name='Показывать слева'),
        ),
        migrations.AddField(
            model_name='projectpage',
            name='project_vitrina',
            field=models.BooleanField(default=False, verbose_name='Показывать витрину'),
        ),
        migrations.AlterField(
            model_name='projectpage',
            name='project_date',
            field=models.DateField(verbose_name='Дата публикации или дата реализации проекта'),
        ),
        migrations.CreateModel(
            name='WorkCategoryList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('projectpage', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='workcategorylist', to='projects.projectpage')),
                ('workcategoryitem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='menuitem.workcategory')),
            ],
            options={
                'verbose_name': 'Список категорий контента',
                'verbose_name_plural': 'Список категорий контента',
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectPageGalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('project_image_caption', models.CharField(blank=True, max_length=250)),
                ('project_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailimages.image')),
                ('project_key', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_gallery_images', to='projects.projectpage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
