from django.db import models
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.models import Page, Orderable, Locale
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel,FieldRowPanel, PageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index
#from menuitem.models import MenuPage импорт в гет контект гдето 105 строка


class ProjectSearch(RoutablePageMixin, Page):
#Не используется
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        projectlist = ProjectPage.objects.all().live().order_by('first_published_at').filter(locale=Locale.get_active())
        context['projectlist'] = projectlist

        return context

    class Meta:
        verbose_name = "Страница поиска"

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
    project_projects = ParentalManyToManyField('projects.ProjectPage', blank=True)
    #intro не используется
    project_intro = RichTextField(blank=True)
    project_vitrina = models.BooleanField(verbose_name="Показывать витрину", default=False)
    project_left = models.BooleanField(verbose_name="Показывать слева", default=False)
    project_slider = models.BooleanField(verbose_name="НЕ показывать слайдер сверху", default=False)
    project_context = models.BooleanField(verbose_name="НЕ показывать результаты контекстного поиска", default=False)

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
            icon = 'image'

    class ImageCenterBlock(blocks.StructBlock):
        imgcenter = ImageChooserBlock()
        imgurl = blocks.URLBlock(required=False)
        txtcenter = blocks.RichTextBlock(required=False)

        class Meta:
            template = 'imgcenter.html'
            icon = 'image'

    project_body = StreamField([
        ('heading', blocks.CharBlock(form_classname="subtitle")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('leftheader', ColumnBlock()),
        ('imageleft', ImageLeftBlock()),
        ('imagecenter', ImageCenterBlock()),
        ('htmlcode', blocks.RawHTMLBlock()),
    ], use_json_field=True, blank=True)

    project_body_bottom = StreamField([
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

        # Фунция выбирает англйиский или русский шаблон грузить
    def get_template(self, request, *args, **kwargs):
        if self.locale.language_code == "en":
            return 'projects\project_page_en.html'
        return 'projects\project_page.html'

    def serve(self, request):
        # Проверяем флаги отправки сообщения
        from news.models import messageshowcheck
        return super().serve(messageshowcheck(request))

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        from menuitem.models import MenuPage
        #Страницы из меню и проектов связанные с текущей
        pagecategory = self.workcategorylist.all()
        if pagecategory:
            if pagecategory.count() > 1:
                menuitemsfilter = MenuPage.objects.live().filter(workcategory_list__workcategoryitem=pagecategory[0].workcategoryitem) | MenuPage.objects.live().filter(workcategory_list__workcategoryitem=pagecategory[1].workcategoryitem)
                projectlist = ProjectPage.objects.live().filter(workcategorylist__workcategoryitem=pagecategory[0].workcategoryitem) | ProjectPage.objects.live().filter(workcategorylist__workcategoryitem=pagecategory[1].workcategoryitem)
            else:
                menuitemsfilter = MenuPage.objects.live().filter(workcategory_list__workcategoryitem=pagecategory[0].workcategoryitem)
                projectlist = ProjectPage.objects.live().filter(workcategorylist__workcategoryitem=pagecategory[0].workcategoryitem)
            menuitemsfilter = menuitemsfilter.filter(locale=Locale.get_active())
            menuitemsfilter = menuitemsfilter.distinct()
            projectlist = projectlist.filter(locale=Locale.get_active())
            projectlist = projectlist.distinct()
            projectlist = projectlist.exclude(id=self.id)
            context['projectlist'] = projectlist
            context['menuitemsfilter'] = menuitemsfilter
      
        childrenpages = self.get_children().live().order_by('first_published_at')
        print(childrenpages)
        context['pagecategory'] = pagecategory
        context['childrenpages'] = childrenpages


        return context

    search_fields = Page.search_fields + [
        index.SearchField('project_header', partial_match=True),
        index.SearchField('project_body', partial_match=True),
        index.SearchField('project_body_bottom', partial_match=True),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('project_header', heading='Расширенный заголовок - показывается на странице, заголовок в меню'),
                FieldPanel('project_date'),
            ],
            heading="Общая информация о странице",
        ),
        #встраиваем список категорий в отдельным блоком в страницу
        InlinePanel('workcategorylist', label="Категория контента"),
        FieldPanel('project_body', heading="Верхний блок контента"),
        FieldPanel('project_body_bottom', heading="Нижний блок контента, после всего"),
        InlinePanel('project_gallery_images', label="Фото галерея"),
        FieldRowPanel(
            [
                FieldPanel('project_vitrina', heading='Показывать дочерние страницы как проекты'),
                FieldPanel('project_left', heading='Показывать ссылки на дочерние страницы в левой колонке'),
                FieldPanel('project_slider', heading='НЕ показывать слайдер'),
                FieldPanel('project_context', heading='НЕ показывать результаты контекстного поиска'),
            ],
            heading="Отображение элементов страницы",
        ),
        MultiFieldPanel(
            [
                FieldPanel('project_avtor', heading='Авторы публикации или участники проекта'),
                FieldPanel('project_projects', heading='Проекты связанные с этой страницей'),
            ],
            heading="Информация о связанных страницах",
        ),

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




