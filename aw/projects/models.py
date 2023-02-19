from django.db import models
from django import forms
from wagtail.models import Page, Orderable, Locale
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index
from wagtail.snippets.models import register_snippet


class WorkCategoryList(Orderable, models.Model):
    projectpage = ParentalKey('projects.ProjectPage', on_delete=models.CASCADE, related_name='workcategorylist')
    workcategoryitem = models.ForeignKey('menuitem.WorkCategory', on_delete=models.CASCADE, related_name='+')

    class Meta(Orderable.Meta):
        verbose_name = "Список категорий контента"
        verbose_name_plural = "Список категорий контента"

    panels = [
        FieldPanel('workcategoryitem', heading='Категории контента'),
    ]

    def __str__(self):
        return self.workcategory.workcategory


class ProjectPage(Page):
    localize_default_translation_mode = "simple"

    project_header = models.CharField(max_length=250, blank=True)
    project_date = models.DateField("Дата публикации или дата реализации проекта")
    project_avtor = ParentalManyToManyField('peoples.PeoplesPage', blank=True)
    #intro не используется
    project_intro = RichTextField(blank=True)
    project_vitrina = models.BooleanField(verbose_name="Показывать витрину", default=False)
    project_left = models.BooleanField(verbose_name="Показывать слева", default=False)

    class ColumnBlock(blocks.StructBlock):
        left = blocks.CharBlock()
        right = blocks.RichTextBlock()

        class Meta:
            template = 'column.html'
            icon = 'user'

    class ImageLeftBlock(blocks.StructBlock):
        imgleft = ImageChooserBlock()
        txtright = blocks.RichTextBlock()

        class Meta:
            template = 'imgleft.html'
            icon = 'user'

    project_body = StreamField([
        ('heading', blocks.CharBlock(form_classname="subtitle")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('leftheader', ColumnBlock()),
        ('imageleft', ImageLeftBlock()),
        ('htmlcode', blocks.RawHTMLBlock()),
    ], use_json_field=True, blank=True)

    def main_image(self):
        gallery_item = self.project_gallery_images.first()
        if gallery_item:
            return gallery_item.project_image
        else:
            return None

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        childrenpages = self.get_children().live().order_by('-first_published_at')
        projectlist = ProjectPage.objects.all().live().order_by('first_published_at').filter(locale=Locale.get_active())

        context['childrenpages'] = childrenpages
        context['projectlist'] = projectlist

        return context

    search_fields = Page.search_fields + [
        index.SearchField('project_header', partial_match=True),
        index.SearchField('project_body', partial_match=True),
    ]



    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('project_header', heading='Расширенный заголовок - показывается на странице, заголовок в меню'),
                FieldPanel('project_date'),
                FieldPanel('project_avtor', heading='Авторы публикации или участники проекта'),
            ],
            heading="Общая информация о странице",
        ),
        MultiFieldPanel(
            [
                FieldPanel('project_vitrina', heading='Показывать дочерние страницы как проекты'),
                FieldPanel('project_left', heading='Показывать ссылки на дочерние страницы в левой колонке'),
            ],
            heading="Отображение дочерних страниц",
        ),
        #встраиваем список категорий в отдельным блоком в страницу
        InlinePanel('workcategorylist', label="Категория контента"),
        FieldPanel('project_body'),
        InlinePanel('project_gallery_images', label="Фото галерея"),
    ]

    class Meta:
        verbose_name = "Страница проекта"
        verbose_name_plural = "Страницы проектов"


class ProjectPageGalleryImage(Orderable):
    project_key = ParentalKey(ProjectPage, on_delete=models.CASCADE, related_name='project_gallery_images')
    project_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    project_image_caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('project_image'),
        FieldPanel('project_image_caption'),
    ]




