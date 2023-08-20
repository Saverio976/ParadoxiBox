from django.http import HttpRequest, HttpResponse
from django.template import loader


def index(request: HttpRequest):
    template = loader.get_template("songs/index.html")
    context = {}
    return HttpResponse(template.render(context, request))


def library_used(request: HttpRequest):
    template = loader.get_template("songs/library_used.html")
    context = {}
    return HttpResponse(template.render(context, request))
