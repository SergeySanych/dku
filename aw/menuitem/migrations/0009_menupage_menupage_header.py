# Generated by Django 4.1.4 on 2023-02-16 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menuitem', '0008_alter_menupage_menupage_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='menupage',
            name='menupage_header',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]