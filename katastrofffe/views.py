from django.shortcuts import render
from django.template.loader import render_to_string
import portfolio


def index_page(request):
    response = portfolio.views.filter_posts(page_number=1)
    posts_template = render_to_string('portfolio/posts_template.html', response)
    response.update({'posts_template': posts_template})
    return render(request, 'index.html', response)


def dev(request):
    response = portfolio.views.filter_posts(page_number=1)
    posts_template = render_to_string('portfolio/posts_template.html', response)
    response.update({'posts_template': posts_template})
    return render(request, 'dev.html', response)


def test(request):
    response = portfolio.views.filter_posts(page_number=1)
    return render(request, 'static.html', response)


def about(request):
    return render(request, 'about.html')


def error404(request):
    return render(request, '404.html', {'object': 'page'})


def error500(request):
    return render(request, '500.html')