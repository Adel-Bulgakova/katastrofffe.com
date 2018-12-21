from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
import portfolio
from portfolio.models import Post, Category
from event.models import Event


def index_page(request):
    response = portfolio.views.filter_posts(page_number=1)
    posts_template = render_to_string('portfolio/posts_template.html', response)
    response.update({'posts_template': posts_template})

    banners = Event.objects.future_events().filter(is_banner=True)
    response.update({'banners': banners})

    return render(request, 'index.html', response)


def dev(request):
    response = portfolio.views.filter_posts(page_number=1)
    posts_template = render_to_string('portfolio/posts_template.html', response)
    response.update({'posts_template': posts_template})

    banners = Event.objects.future_events().filter(is_banner=True)
    response.update({'banners': banners})

    return render(request, 'dev.html', response)


def test(request):
    response = portfolio.views.filter_posts(page_number=1)
    return render(request, 'static.html', response)


def google_verification(request):
    return render(request, 'googleb758d0ca397ee06d.html')


def about(request):
    return render(request, 'about.html')


def error404(request):
    return render(request, '404.html', {'object': 'page'})


def error500(request):
    return render(request, '500.html')


def privacy_policy(request):
    return render(request, 'privacy_policy.html')


def terms_of_service(request):
    return render(request, 'terms_of_service.html')