from django.shortcuts import redirect


def redirect_api_docs(_):
    response = redirect("/api/docs")
    return response
