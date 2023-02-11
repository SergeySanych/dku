from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index


class MenuPage(Page):
    menupage_date = models.DateField("Post date")
    menupage_body = StreamField([
        ('heading', blocks.CharBlock(form_classname="subtitle")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], use_json_field=True)

    search_fields = Page.search_fields + [
        index.SearchField('menupage_body', partial_match=True),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('menupage_date'),
        FieldPanel('menupage_body'),
    ]

