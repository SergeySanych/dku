# Generated by Django 4.1.4 on 2023-02-02 06:12

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0078_referenceindex'),
        ('news', '0016_alter_internalpage_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='internalpage',
            name='related_pages',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, null=True, related_name='+', to='wagtailcore.page'),
        ),
    ]