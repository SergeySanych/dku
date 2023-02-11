# Generated by Django 4.1.4 on 2023-02-05 08:31

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0078_referenceindex'),
        ('news', '0017_internalpage_related_pages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internalpage',
            name='related_pages',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, related_name='+', to='wagtailcore.page'),
        ),
    ]
