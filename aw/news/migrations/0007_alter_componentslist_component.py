# Generated by Django 4.1.4 on 2023-01-18 09:53

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_componentslist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='componentslist',
            name='component',
            field=wagtail.fields.RichTextField(blank=True),
        ),
    ]
