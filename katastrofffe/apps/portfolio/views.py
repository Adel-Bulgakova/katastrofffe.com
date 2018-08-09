# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.template.loader import render_to_string
from .models import Category, Post, PostMediaData
from katastrofffe import views
import math


def categories_list(request):
    categories = Category.objects.published().filter(parent=None)

    return render(request, 'portfolio/categories_list.html', {'categories': categories})


def get_pages_count(filter_name='', filter_data=''):
    posts_on_page_count = settings.POSTS_ON_PAGE_COUNT

    if filter_name == 'tag':
        posts_count = len(Post.objects.published().filter(tags__name__in=[filter_data]))

    elif filter_name == 'category':
        category = Category.objects.get(slug=filter_data)
        posts_count = len(Post.objects.published().filter(category=category))

    else:
        posts_count = len(Post.objects.published().all())

    pages_count = int(math.ceil(posts_count/posts_on_page_count) + 1)
    return pages_count


def filter_posts(page_number=1, filter_name='', filter_data=''):
    response = {}

    posts_on_page_count = settings.POSTS_ON_PAGE_COUNT

    page = int(page_number)
    slice_from = (page - 1) * posts_on_page_count
    slice_to = page * posts_on_page_count

    posts = {}
    try:
        if filter_name == 'tag':
            posts = Post.objects.published().filter(tags__name__in=[filter_data])[slice_from:slice_to]
            pages_count = get_pages_count(filter_name='tag', filter_data=filter_data)
            response.update({'pages_count': pages_count})
            response.update({'tag_name': filter_data})
        elif filter_name == 'category':
            category = Category.objects.get(slug=filter_data)
            posts = Post.objects.published().filter(category=category)[slice_from:slice_to]
        else:
            pages_count = get_pages_count()
            response.update({'pages_count': pages_count})
            posts = Post.objects.published().all()[slice_from:slice_to]
    finally:
        response.update({'posts': posts})

    categories_data = Category.objects.published().filter(parent=None)
    response.update({'categories': categories_data})

    return response


def show_category(request, hierarchy=None):
    category_slug = hierarchy.split('/')
    parent = None
    root = Category.objects.all()

    for slug in category_slug[:-1]:
        try:
            parent = root.get(parent=parent, slug=slug)
        except:
            return render(request, '404.html', {'object':'post'})

    try:
        instance = Category.objects.get(parent=parent, slug=category_slug[-1])
    except:
        slug = category_slug[-1]
        try:
            instance = Post.objects.get(slug=slug)
            post_media = instance.get_post_media
            return render(request, 'portfolio/post_detail.html', {'post': instance, 'post_media': post_media})
        except:
            return render(request, '404.html', {'object':'post'})
    else:
        category_slug = instance.slug
        slice_to = settings.POSTS_ON_PAGE_COUNT
        posts = Post.objects.published().filter(category=instance)[:slice_to]
        pages_count = get_pages_count(filter_name='category', filter_data=category_slug)
        posts_template = render_to_string('portfolio/posts_template.html', {'posts':posts})
        return render(request, 'portfolio/category_detail.html', {'category':instance, 'categories': root, 'pages_count': pages_count, 'posts':posts, 'posts_template':posts_template})


def tag_detail(request, page_number=1, tag_name=''):
    response = filter_posts(page_number=page_number, filter_name='tag', filter_data=tag_name)
    posts_template = render_to_string('portfolio/posts_template.html', response)
    response.update({'posts_template': posts_template})
    return render(request, 'portfolio/tag_detail.html', response)


def filter_by_category(request, page_number=1, category_slug=''):
    response = filter_posts(page_number=page_number, filter_name='category', filter_data=category_slug)
    return render(request, 'portfolio/posts_template.html', response)


def filter_by_tag(request, page_number=1, tag_name=''):
    response = filter_posts(page_number=page_number, filter_name='tag', filter_data=tag_name)
    return render(request, 'portfolio/posts_template.html', response)


def filter_by_page(request, page_number=1):
    response = filter_posts(page_number=page_number, filter_name='', filter_data='')
    return render(request, 'portfolio/posts_template.html', response)