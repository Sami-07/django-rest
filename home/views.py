from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response



@api_view(["GET", "POST", "PUT", "PATCH", "DELETE"])
def index(request):
    dict = {
        "name": "Sami",
        "role": "Tech Lead",
        "company": "WiseIN",
        "skills": ["TypeScript", "Next.js"]
    }
    if(request.method == "GET"):
        print("GET request")
        return Response(dict)
    elif(request.method == "POST"):
        print("POST request")
        return Response(dict)
    elif(request.method == "PUT"):
        print("PUT request")
        return Response(dict)

