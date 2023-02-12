from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index


class ProjectPage(Page):
    project_date = models.DateField("Дата реализации проекта")
    project_intro = RichTextField(blank=True)
