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
    left = blocks.CharBlock(help_text='Заголовок блока', required=False)
    leftrich = blocks.RichTextBlock(help_text='Форматированый блок под заголовком слева', required=False)
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


class NewsBlock(blocks.StructBlock):
    header = blocks.TextBlock(required=False)

    newslist = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("pic", ImageChooserBlock(help_text='Изображение для новости')),
                ("newsheader", blocks.TextBlock(max_length=250)),
                ("url", blocks.TextBlock(help_text='Ссылка на нужную страницу, можно другой сайт', max_length=250) )
            ]
        )
    )

    class Meta:
        template = 'newslist.html'
        icon = 'check'
        label = 'NewsList'


class FilterBlock(blocks.StructBlock):
    filterlevel = blocks.IntegerBlock(help_text='1 or 2 - levels', default=1)
    filterall = blocks.CharBlock(help_text='Текст для ВСЕ', default='ВСЕ')

    filterlist1 = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("fl1_name", blocks.TextBlock(help_text='Название фильтра')),
                ("fl1_code", blocks.TextBlock(help_text='Код фильтра уникальный латинскими буквами, короткий')),
            ]
        )
    )

    filterlist2 = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("fl2_name", blocks.TextBlock(help_text='Название фильтра')),
                ("fl2_code", blocks.TextBlock(help_text='Код фильтра уникальный латинскими буквами, короткий')),
                ("fl2_fl1_code", blocks.TextBlock(help_text='Код фильтра уникальный латинскими буквами, короткий')),
            ]
        )
    )

    filterlistdata = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("fld_name", blocks.TextBlock(help_text='Название')),
                ("fld_code1", blocks.TextBlock(help_text='Код из первого списка')),
                ("fld_code2", blocks.TextBlock(help_text='Код из первого списка', required=False)),
                ("fld_url", blocks.TextBlock(help_text='Ссылка на сайт', required=False)),
                ("fld_logo", ImageChooserBlock(help_text='Логотип квадратный', required=False)),
            ]
        )
    )

    class Meta:
        template = 'filter.html'
        icon = 'check'
        label = 'Filter'


class WideSliderBlock(blocks.StructBlock):
    wideslider = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("pic", ImageChooserBlock(required=True)),
            ]
        )
    )

    class Meta:
        template = 'wideslider.html'
        icon = 'placeholder'
        label = 'WideSlider'


@register_snippet
class MinisiteList(ClusterableModel):
    minisite_name = models.CharField(max_length=50)
    minisite_header_ru = models.CharField(max_length=250, null=True, blank=True)
    minisite_header_en = models.CharField(max_length=250, null=True, blank=True)
    minisite_subheader_ru = models.CharField(max_length=250, null=True, blank=True)
    minisite_subheader_en = models.CharField(max_length=250, null=True, blank=True)

    minisite_listlogo = models.BooleanField(verbose_name="Показывать список логотипов вверху", default=False)
    minisite_listlogo_bottom = models.BooleanField(verbose_name="Показывать список логотипов внизу", default=False)

    minisite_fonblock = models.BooleanField(verbose_name="Показывать блок с фоновым рисунком и заголовком сайта", default=True)
    minisite_fon_color = models.CharField(max_length=15, null=True, blank=True, default='#fafafa')
    minisite_fon_textcolor = models.CharField(max_length=15, null=True, blank=True, default='#2165AD')

    minisite_leftlogo = models.BooleanField(verbose_name="Показывать блок с логотипом слева и заголовком сайта", default=False)
    minisite_ll_fon_color = models.CharField(max_length=15, null=True, blank=True, default='#fafafa')
    minisite_ll_textcolor = models.CharField(max_length=15, null=True, blank=True, default='#2165AD')

    minisite_mainlogo = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )


    panels = [
        FieldPanel('minisite_name', heading="Короткое название сайта, как в домене"),
        FieldPanel('minisite_header_ru', heading="Заголовок мини сайта на русском"),
        FieldPanel('minisite_header_en', heading="Заголовок мини сайта на английском"),
        FieldPanel('minisite_subheader_ru', heading="ПодЗаголовок мини сайта на русском"),
        FieldPanel('minisite_subheader_en', heading="ПодЗаголовок мини сайта на английском"),


        MultiFieldPanel(
            [
                FieldPanel('minisite_listlogo', heading="Показывать список логотипов вверху"),
                FieldPanel('minisite_listlogo_bottom', heading="Показывать список логотипов внизу"),
                InlinePanel('minisite_gallery_images', label="Список логотипов"),
            ],
            heading="Блок логотипов",
            classname="collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel('minisite_fonblock', heading="Показывать блок с фоновым рисунком и заголовком сайта"),
                FieldPanel('minisite_fon_color', heading="Цвет фона в шестнадцетеричном формате"),
                FieldPanel('minisite_fon_textcolor', heading="Цвет текста в шестнадцетеричном формате"),
            ],
            heading="Блок с фоновым рисунком и заголовком сайта",
            classname="collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel('minisite_leftlogo', heading="Показывать блок с логотипом слева и заголовком сайта"),
                FieldPanel('minisite_mainlogo', heading="Основной логотип минисайта"),
                FieldPanel('minisite_ll_fon_color', heading="Цвет фона в шестнадцетеричном формате"),
                FieldPanel('minisite_ll_textcolor', heading="Цвет текста в шестнадцетеричном формате"),
            ],
            heading="Блок с логотипом слева и заголовком сайта",
            classname="collapsed",
        ),

    ]

    def __str__(self):
        return self.minisite_name

    class Meta:
        verbose_name_plural = 'Minisite list'
        verbose_name = 'Minisite list'


class MinisitePage(Page):

    # Фунция выбирает англйиский или русский шаблон грузить
    def get_template(self, request, *args, **kwargs):
        if self.locale.language_code == "en":
            return 'minisite/minisite_page_en.html'
        return 'minisite/minisite_page.html'

    minisite = models.ForeignKey(
        MinisiteList,
        on_delete=models.PROTECT,
        related_name='minisite_pages'
    )

    minisite_bgimage = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    minisite_title_h1 = models.CharField(max_length=255, null=True, blank=True)
    minisite_news = models.BooleanField(verbose_name="Показывать новости", default=False)
    minisite_onecolumn = models.BooleanField(verbose_name="Показывать блок во всю ширину экрана", default=False)
    minisite_twocolumn = models.BooleanField(verbose_name="Показывать блок в две колонки", default=False)

    minisite_body = StreamField([
            ('heading', blocks.CharBlock(form_classname="subtitle")),
            ('paragraph', blocks.RichTextBlock()),
            ('image', ImageChooserBlock()),
            ('htmlcode', blocks.RawHTMLBlock()),
            ('filter', FilterBlock()),
            ('leftheader2', LeftHeaderBlock()),
            ('checklist2', CheckListBlock2()),
            ('newsblock', NewsBlock()),
            ('wideslider', WideSliderBlock()),
        ], use_json_field=True, blank=True)

    minisite_leftbody = StreamField([
            ('heading', blocks.CharBlock(form_classname="subtitle")),
            ('paragraph', blocks.RichTextBlock()),
            ('image', ImageChooserBlock()),
            ('htmlcode', blocks.RawHTMLBlock()),
            ('filter', FilterBlock()),
            ('leftheader2', LeftHeaderBlock()),
            ('checklist2', CheckListBlock2()),
            ('newsblock', NewsBlock()),
            ('wideslider', WideSliderBlock()),
        ], use_json_field=True, blank=True)

    minisite_rightbody = StreamField([
        ('heading', blocks.CharBlock(form_classname="subtitle")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('htmlcode', blocks.RawHTMLBlock()),
        ('filter', FilterBlock()),
        ('leftheader2', LeftHeaderBlock()),
        ('checklist2', CheckListBlock2()),
        ('newsblock', NewsBlock()),
        ('wideslider', WideSliderBlock()),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('minisite',  heading='Выбор мини-сайта'),
        FieldPanel('minisite_bgimage', heading='Фоновый рисунок'),
        FieldPanel('minisite_title_h1', heading='Заголовок страницы'),
        FieldPanel('minisite_news', heading='Показывать новости'),
        MultiFieldPanel(
            [
                FieldPanel('minisite_onecolumn', heading="Показывать блок во всю ширину экрана"),
                FieldPanel('minisite_body', heading='Контент блок'),
            ],
            heading="Блок во всю ширину экрана",
            classname="collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel('minisite_twocolumn', heading="Показывать блок в две колонки"),
                FieldPanel('minisite_leftbody', heading='Контент блок для левой колонки'),
                FieldPanel('minisite_rightbody', heading='Контент блок для правой колонки'),
            ],
            heading="Блок в две колонки",
            classname="collapsed",
        ),

    ]


class MiniSiteGalleryImage(Orderable):
    minisite_key = ParentalKey(MinisiteList, on_delete=models.CASCADE, related_name='minisite_gallery_images')
    minisite_logo = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )

    panels = [
        FieldPanel('minisite_logo'),
    ]

