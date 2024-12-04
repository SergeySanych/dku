from django.db import models
from django import forms
from django.shortcuts import redirect
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.models import Page, Orderable, Locale
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel, FieldRowPanel
from wagtail.admin.edit_handlers import PageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.search.backends.database.postgres.postgres import PostgresSearchQueryCompiler
from projects.models import ProjectPage
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.settings.models import BaseSetting, register_setting

# Partial search bug fix
PostgresSearchQueryCompiler.LAST_TERM_IS_PREFIX = True


@register_snippet
class Tags(models.Model):
    tag_name_ru = models.CharField(max_length=255, verbose_name="Название тега на русском")
    tag_name_en = models.CharField(max_length=255, verbose_name="Название тега на английском")

    search_fields = Page.search_fields + [
        index.SearchField('tag_name_ru'),
        index.SearchField('tag_name_en'),
    ]

    panels = [
        FieldPanel('tag_name_ru'),
        FieldPanel('tag_name_en'),
    ]

    def __str__(self):
        return self.tag_name_ru

    class Meta:
        verbose_name_plural = 'Теги'


def messageshowcheck(request):
    """

    :type request: object
    """
    # Функция проверяет флаги перехода на после отправки сообщения с сайта.
    # ошибка на случай если переменые еще не созданы
    print("Serve!!!")
    try:
        if request.session['form_page_success'] == True & request.session['message_show'] == True:
            request.session['form_page_success'] = False
            return request
        else:
            request.session['message_show'] = True
            return request
    except KeyError:
        print("KeyError!!!")
        pass
    return request


class NewsIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_template(self, request, *args, **kwargs):
        if self.locale.language_code == "en":
            return 'news/news_index_page_en.html'
        return 'news/news_index_page.html'

    def get_context(self, request):
        print("get_context!!!")
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        newspages = self.get_children().live().order_by('-first_published_at')
        tags = Tags.objects.all()
        context['newspages'] = newspages
        context['tags'] = tags
        return context

    def serve(self, request):
        # Проверяем флаги отправки сообщения
        return super().serve(messageshowcheck(request))

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]


class NewsPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'NewsPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class NewsPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=NewsPageTag, blank=True)
    categories = ParentalManyToManyField('news.NewsCategory', blank=True)
    news_tags = ParentalManyToManyField('news.Tags', blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    def serve(self, request):
        # Проверяем флаги отправки сообщения
        return super().serve(messageshowcheck(request))

    def get_context(self, request):
        context = super().get_context(request)
        context['newspages'] = ProjectPage.objects.all().live().order_by('first_published_at').filter(
            locale=Locale.get_active())
        # Update context to include only published posts, ordered by reverse-chron
        #Вместо дочерних здесь берем братьев и сестер
        childrenpages = self.get_siblings().all().live().order_by('-first_published_at')[:6]

        #projectlist = ProjectPage.objects.all().live().order_by('first_published_at').filter(locale=Locale.get_active())
        context['childrenpages'] = childrenpages

        return context

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date', heading="Дата выхода новости"),
        ], heading="Blog information"),
        FieldPanel('news_tags', heading='Теги новостей', widget=forms.CheckboxSelectMultiple),
        FieldPanel('intro', heading="Обезательное поле, отображается на главной (анонс новости)"),
        FieldPanel('body', heading="Текст новости"),
        InlinePanel('gallery_images', label="Изображение - отображается на главной"),
    ]


class NewsPageGalleryImage(Orderable):
    page = ParentalKey(NewsPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]


class MainPage(Page):
    # Fileds for article in kmoweldge space
    articletext = models.CharField(max_length=255, null=True, blank=True)
    articleurl = models.CharField(max_length=255, null=True, blank=True)
    articleimage = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    # Fileds for jurnal in kmoweldge space
    jurnaltext = models.CharField(max_length=255, null=True, blank=True)
    jurnalurl = models.CharField(max_length=255, null=True, blank=True)
    jurnalimage = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    # Fileds for analytic notes in kmoweldge space
    notestext = models.CharField(max_length=255, null=True, blank=True)
    notesurl = models.CharField(max_length=255, null=True, blank=True)
    notesimage = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    # Fileds for podcasts in kmoweldge space
    podcaststext = models.CharField(max_length=255, null=True, blank=True)
    podcastsurl = models.CharField(max_length=255, null=True, blank=True)
    podcastsimage = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    # Fileds for publics in kmoweldge space
    publicstext = models.CharField(max_length=255, null=True, blank=True)
    publicsurl = models.CharField(max_length=255, null=True, blank=True)
    publicsimage = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    components = ParentalManyToManyField('news.ComponentsList', blank=True)

    #Фунция выбирает англйиский или русский шаблон грузить
    def get_template(self, request, *args, **kwargs):
        if self.locale.language_code == "en":
            return 'news/main_page_en.html'
        return 'news/main_page.html'

    def serve(self, request):
        # Проверяем флаги отправки сообщения
        return super().serve(messageshowcheck(request))

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('components', widget=forms.CheckboxSelectMultiple),
        ], heading="Components list"),
        MultiFieldPanel([
            FieldPanel('articletext'),
            FieldPanel('articleurl'),
            FieldPanel('articleimage'),
        ], heading="Статья для блока центр знаний"),
        MultiFieldPanel([
            FieldPanel('jurnaltext'),
            FieldPanel('jurnalurl'),
            FieldPanel('jurnalimage'),
        ], heading="Блок журнала"),
        MultiFieldPanel([
            FieldPanel('notestext'),
            FieldPanel('notesurl'),
            FieldPanel('notesimage'),
        ], heading="Блок аналитические записки"),
        MultiFieldPanel([
            FieldPanel('podcaststext'),
            FieldPanel('podcastsurl'),
            FieldPanel('podcastsimage'),
        ], heading="Блок подкасты"),
        MultiFieldPanel([
            FieldPanel('publicstext'),
            FieldPanel('publicsurl'),
            FieldPanel('publicsimage'),
        ], heading="Блок другие публикации"),
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        lastnews = NewsPage.objects.all().live().order_by('-first_published_at').filter(locale=Locale.get_active())[:4]
        context['lastnews'] = lastnews
        return context


class NewsTagIndexPage(Page):

    def get_context(self, request):
        # Filter by tag
        tag = request.GET.get('tag')
        # newspages = NewsPage.objects.filter(tags__name=tag)
        newspages = NewsPage.objects.all()
        # Update template context
        context = super().get_context(request)
        context['newspages'] = newspages
        return context


@register_snippet
class NewsCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'blog categories'


@register_snippet
class ComponentsList(models.Model):
    componentname = models.CharField(max_length=50, null=True, blank=True)
    component = RichTextField(blank=True)
    picture = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    related_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = [
        FieldPanel('componentname'),
        FieldPanel('component'),
        FieldPanel('picture'),
        PageChooserPanel('related_page'),
    ]

    def __str__(self):
        return self.componentname

    class Meta:
        verbose_name_plural = 'Key components list'


# InternalPage удалиьть когда уберу страницы связанные с ней
class InternalPage(Page):
    class ColumnBlock(blocks.StructBlock):
        left = blocks.CharBlock()
        right = blocks.RichTextBlock()

        class Meta:
            template = 'column.html'
            icon = 'user'

    related_pages = ParentalManyToManyField(
        'wagtailcore.Page',
        blank=True,
        related_name='+',
    )
    date = models.DateField("Post date")
    body = StreamField([
        ('column', blocks.ListBlock(ColumnBlock())),
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], use_json_field=True)

    search_fields = Page.search_fields + [
        index.SearchField('title', partial_match=True),
        index.AutocompleteField('title'),
        index.SearchField('body', partial_match=True),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        PageChooserPanel('related_pages'),
        FieldPanel('body'),
    ]


@register_setting
class MyAppSettings(BaseSetting):
    # relationship to a single form page (one per site)
    modal_form_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Modal Form'
    )

    panels = [
        # note the kwarg - this will only allow form pages to be selected (replace base with your app)
        PageChooserPanel('modal_form_page', page_type='news.FormPage')
    ]


#поля для формы отправки сообщения
class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')


#Страница формы сообщения
class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

    def render_landing_page(self, request, form_submission=None, *args, **kwargs):
        #Вызывается для отрисовки посадочной, у нас переадресация на текущую страницу
        print('Рендеринг лендинга')
        source_page_id = request.POST.get('source-page-id')
        print(source_page_id)

        if int(source_page_id) == 0:
            request.session['form_page_success'] = True
            request.session['message_show'] = False
            print(request.session['form_page_success'])
            print(request.session['message_show'])
            print("/"+self.locale.language_code+"/search/")
            return redirect("/"+self.locale.language_code+"/search/", permanent=False)
        else:
            source_page = Page.objects.get(pk=source_page_id)
            request.session['form_page_success'] = True
            request.session['message_show'] = False
            print(source_page.url)
            return redirect(source_page.url, permanent=False)

        # if no source_page is set, render default landing page
        return super().render_landing_page(request, form_submission, *args, **kwargs)
