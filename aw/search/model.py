from django.db import models
from wagtail.models import Page, Orderable, Locale
from projects.models import ProjectPage


class Search(Page):
    search_header = models.CharField(max_length=250, blank=True)

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        projectlist = ProjectPage.objects.all().live().order_by('first_published_at').filter(locale=Locale.get_active())
        context['projectlist'] = projectlist

        return context

    class Meta:
        verbose_name = "Страница поиска"

