from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response



@api_view(["GET"])
def index(request):
    dict = {
        "name": "Sami",
        "role": "Tech Lead",
        "company": "WiseIN",
        "skills": ["TypeScript", "Next.js"]
    }
    return Response(dict)
