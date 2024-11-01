from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse
from django.db import models
from wagtail.models import Page, Locale
from wagtail.search.models import Query


def search(request):
    print("SEARCH")
    from news.models import messageshowcheck
    request = messageshowcheck(request)
    #Проверка флагов показа отправки сообщения
    search_query = request.GET.get("query", None)
    #запрос страницы пагинации
    page = request.GET.get("page", 1)
    lcode = Locale.get_active().language_code
    if lcode == "en":
        rf = False
    else:
        rf = True
    # Search
    if search_query:
        search_results = Page.objects.live().search(search_query, operator="or")
        query = Query.get(search_query)

        # Record hit
        query.add_hit()
    else:
        search_results = Page.objects.none()

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    if lcode == "ru":
        return TemplateResponse(
            request,
            "search/search.html",
            {
                "search_query": search_query,
                "search_results": search_results,
                "lcode": lcode,
            },
        )
    else:
        return TemplateResponse(
            request,
            "search/search_en.html",
            {
                "search_query": search_query,
                "search_results": search_results,
                "lcode": lcode,
            },
        )


