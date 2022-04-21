from django.shortcuts import render
from .models import BlogContent, PageHeading, BackgroundImage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404


# Create your views here.
def blog(request):
    template = 'blog/blog.html'

    blog_obj = BlogContent.objects.all().order_by('-date')
    blog_heading = PageHeading.objects.last()
    bg_image = BackgroundImage.objects.last()

    latest_blog = BlogContent.objects.all().order_by('-date')[:3]

    try:
        paginator = Paginator(blog_obj, 4)  
        page = request.GET.get('page')
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    except:
        raise Http404("Something went wrong.")

    context={
        'page_obj': page_obj,
        'latest_blog': latest_blog,
        'blog_heading': blog_heading,
        'bg_image': bg_image,
    }

    return render(request, template, context)

def blog_detail(request, pk):
    template = 'blog/blog_detail.html'

    blog_detail = BlogContent.objects.get(id = pk)
    blog_heading = PageHeading.objects.last()
    bg_image = BackgroundImage.objects.last()

    blog_obj = BlogContent.objects.all().order_by('-date')
    latest_blog = BlogContent.objects.all().order_by('-date')[:3]

    context = {
        'blog_detail': blog_detail,
        'latest_blog': latest_blog,
        'bg_image': bg_image,
        'blog_heading': blog_heading,
    }

    return render(request, template, context)


