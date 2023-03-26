from django.db import models
from django import forms
from wagtail.snippets.models import register_snippet
from wagtail.models import Page, Locale, Orderable
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index


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

    search_fields = Page.search_fields + [
        index.SearchField('full_name'),
        index.SearchField('full_discription'),
    ]

    def serve(self, request):
        # Проверяем флаги отправки сообщения
        from news.models import messageshowcheck
        return super().serve(messageshowcheck(request))

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('full_name'),
            FieldPanel('people_categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Основная информация"),
        FieldPanel('short_discription'),
        FieldPanel('full_discription'),
        FieldPanel('photo'),
    ]


class PeoplesTeamPage(Page):
    team_discription = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('team_discription'),
    ]

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

    def get_context(self, request):
        researcherpages = PeoplesPage.objects.all().live().order_by('first_published_at').filter(locale=Locale.get_active())
        context = super().get_context(request)
        context['researchers'] = researcherpages.filter(people_categories__peoplecategory='Научные сотрудники')
        return context

