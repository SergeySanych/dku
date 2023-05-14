from django.db import models
from django import forms
from wagtail.snippets.models import register_snippet
from wagtail.models import Page, Locale, Orderable
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index

from menuitem.models import MenuPage
from projects.models import ProjectPage


@register_snippet
class PeoplesCategory(models.Model):
    peoplecategory = models.CharField(max_length=255)

    panels = [
        FieldPanel('peoplecategory'),
    ]

    def __str__(self):
        return self.peoplecategory

    class Meta:
        verbose_name_plural = 'Группы людей'


class PeoplesPage(Page):
    full_name = models.CharField(max_length=250)
    photo = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    short_discription = RichTextField(blank=True)
    full_discription = RichTextField(blank=True)
    people_categories = ParentalManyToManyField('peoples.PeoplesCategory', blank=True)
    people_projects = ParentalManyToManyField('projects.ProjectPage', blank=True)
    search_fields = Page.search_fields + [
        index.SearchField('full_name'),
        index.SearchField('full_discription'),
    ]

    #Фунция выбирает англйиский или русский шаблон грузить
    def get_template(self, request, *args, **kwargs):
        if self.locale.language_code == "en":
            return 'peoples/peoples_page_en.html'
        return 'peoples/peoples_page.html'

    def serve(self, request):
        # Проверяем флаги отправки сообщения
        from news.models import messageshowcheck
        return super().serve(messageshowcheck(request))

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        #Вместо дочерних здесь берем братьев и сестер
        childrenpages = self.get_siblings().all().live().order_by('first_published_at')

        #projectlist = ProjectPage.objects.all().live().order_by('first_published_at').filter(locale=Locale.get_active())
        context['childrenpages'] = childrenpages

        return context

    content_panels = Page.content_panels + [
        FieldPanel('full_name'),
        FieldPanel('short_discription'),
        FieldPanel('full_discription'),
        FieldPanel('photo'),
        MultiFieldPanel([
            FieldPanel('people_categories', widget=forms.CheckboxSelectMultiple),
            FieldPanel('people_projects', heading='Участие в проектах'),
        ], heading="Дополнительная информация"),
    ]


class PeoplesTeamPage(Page):
    team_discription = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('team_discription'),
    ]

    #Фунция выбирает англйиский или русский шаблон грузить
    def get_template(self, request, *args, **kwargs):
        if self.locale.language_code == "en":
            return 'peoples/peoples_team_page_en.html'
        return 'peoples/peoples_team_page.html'


    def serve(self, request):
        # Проверяем флаги отправки сообщения
        from news.models import messageshowcheck
        return super().serve(messageshowcheck(request))

    def get_context(self, request):
        teamspages = PeoplesPage.objects.all().live().order_by('first_published_at').filter(locale=Locale.get_active())
        context = super().get_context(request)
        context['teampeoples'] = teamspages.filter(people_categories__peoplecategory='Наша команда')
        return context


class PeoplesResearcherPage(Page):
    researcher_description = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('researcher_description'),
    ]

    def serve(self, request):
        # Проверяем флаги отправки сообщения
        from news.models import messageshowcheck
        return super().serve(messageshowcheck(request))

    #Фунция выбирает англйиский или русский шаблон грузить
    def get_template(self, request, *args, **kwargs):
        if self.locale.language_code == "en":
            return 'peoples/peoples_researcher_page_en.html'
        return 'peoples/peoples_researcher_page.html'

    def get_context(self, request):
        researcherpages = PeoplesPage.objects.all().live().order_by('first_published_at').filter(locale=Locale.get_active())
        context = super().get_context(request)
        context['researchers'] = researcherpages.filter(people_categories__peoplecategory='Научные сотрудники')
        return context

