from django.db import models
from modelcluster.models import ClusterableModel
from wagtail.snippets.models import register_snippet
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel, FieldRowPanel
from wagtail.models import Page, Orderable, Locale
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class LeftHeaderBlock(blocks.StructBlock):
    left = blocks.CharBlock(required=False)
    header_level = blocks.IntegerBlock(help_text='Уровень заголовка', min_value=1, max_value=4, default=3)
    # 1 - blue, 2 - red
    color = blocks.IntegerBlock(help_text='0 - no, 1 - blue, 2 - red', default=0)
    # 0 - no, 1 - external, 2 - internal
    position = blocks.IntegerBlock(help_text='0 - no, 1 - external, 2 - internal', default=0)
    right = blocks.RichTextBlock(required=False)
    # 0 - no, 1 - blue, 2 - red
    rightcolor = blocks.IntegerBlock(help_text='0 - no, 1 - blue, 2 - red', default=0)
    rightborder = blocks.RichTextBlock(required=False)
    rightfinish = blocks.RichTextBlock(required=False)
    cta = blocks.CharBlock(required=False)
    url = blocks.CharBlock(required=False)

    class Meta:
        template = 'leftheader.html'
        icon = 'list-ul'
        label = 'LeftHeader with border'


class OneCheckListBlock(blocks.StructBlock):
    listheader = blocks.RichTextBlock(required=False)

    checklist = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("checktext", blocks.RichTextBlock(required=False)),
                ("text", blocks.RichTextBlock(required=False)),
            ]
        )
    )

    class Meta:
        template = 'onechecklist.html'
        icon = 'check'
        label = 'OneCheckList'


class CheckListBlock2(blocks.StructBlock):
    bgimage = ImageChooserBlock()
    header = blocks.CharBlock()
    beforechecklisttext = blocks.TextBlock(required=False)
    afterchecklisttext = blocks.TextBlock(required=False)

    checklist = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("inchecklist", OneCheckListBlock()),
            ]
        )
    )

    class Meta:
        template = 'checklist2.html'
        icon = 'check'
        label = 'CheckList2'


class CheckListBlock(blocks.StructBlock):
    bgimage = ImageChooserBlock()
    header = blocks.CharBlock()
    beforechecklisttext = blocks.TextBlock(required=False)
    afterchecklisttext = blocks.TextBlock(required=False)

    checklist = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("checktext", blocks.RichTextBlock(required=False, max_length=250)),
                ("text", blocks.TextBlock(required=False, max_length=250)),
            ]
        )
    )

    class Meta:
        template = 'checklist.html'
        icon = 'check'
        label = 'CheckList'


@register_snippet
class MinisiteList(ClusterableModel):
    minisite_name = models.CharField(max_length=50)
    minisite_header_ru = models.CharField(max_length=250, null=True, blank=True)
    minisite_header_en = models.CharField(max_length=250, null=True, blank=True)
    minisite_subheader_ru = models.CharField(max_length=250, null=True, blank=True)
    minisite_subheader_en = models.CharField(max_length=250, null=True, blank=True)

    panels = [
        FieldPanel('minisite_name', heading="Короткое название сайта, как в домене"),
        FieldPanel('minisite_header_ru', heading="Заголовок мини сайта на русском"),
        FieldPanel('minisite_header_en', heading="Заголовок мини сайта на английском"),
        FieldPanel('minisite_subheader_ru', heading="ПодЗаголовок мини сайта на русском"),
        FieldPanel('minisite_subheader_en', heading="ПодЗаголовок мини сайта на английском"),

        InlinePanel('minisite_gallery_images', label="Список логотипов"),
    ]

    def __str__(self):
        return self.minisite_name

    class Meta:
        verbose_name_plural = 'Minisite list'
        verbose_name = 'Minisite list'


class MinisitePage(Page):
    minisite = models.ForeignKey(
        MinisiteList,
        on_delete=models.CASCADE,
        related_name='minisite_pages'
    )

    minisite_bgimage = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    minisite_title_h1 = models.CharField(max_length=255, null=True, blank=True)
    minisite_news = models.BooleanField(verbose_name="Показывать новости", default=False)

    minisite_body = StreamField([
            ('heading', blocks.CharBlock(form_classname="subtitle")),
            ('paragraph', blocks.RichTextBlock()),
            ('image', ImageChooserBlock()),
            ('htmlcode', blocks.RawHTMLBlock()),
            ('image', ImageChooserBlock()),
            ('leftheader2', LeftHeaderBlock()),
            ('checklist2', CheckListBlock2()),
        ], use_json_field=True, blank=True)


    content_panels = Page.content_panels + [
        FieldPanel('minisite',  heading='Выбор мини-сайта'),
        FieldPanel('minisite_bgimage', heading='Фоновый рисунок'),
        FieldPanel('minisite_title_h1', heading='Заголовок страницы'),
        FieldPanel('minisite_news', heading='Показывать новости'),
        FieldPanel('minisite_body', heading='Контент блок'),
    ]


class MiniSiteGalleryImage(Orderable):
    minisite_key = ParentalKey(MinisiteList, on_delete=models.CASCADE, related_name='minisite_gallery_images')
    minisite_logo = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )

    panels = [
        FieldPanel('minisite_logo'),
    ]

