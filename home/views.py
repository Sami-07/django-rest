from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Person
from .serializers import PeopleSerializer, LoginSerializer, RegisterSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication   
class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data = data)
        if(not serializer.is_valid()):
             return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username = data["username"], password = data["password"])
        if not user:
            return Response({"error" : "User not found"}, status=status.HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user = user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)
        
class RegisterAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if (not serializer.is_valid()):
            return Response({"error": serializer.errors,  "user_created": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"data": serializer.data, "user_created": True}, status=status.HTTP_201_CREATED)


@api_view(["GET", "POST", "PUT", "PATCH", "DELETE"])
def index(request):
    """
    Base API endpoint that handles multiple HTTP methods.
    GET: Returns a sample dictionary with user information
    POST: Returns the received data back to the client
    PUT: Returns a sample dictionary (currently same as GET response)
    """
    dict = {
        "name": "Sami",
        "age": 20
    }
    if (request.method == "GET"):
        print("GET request")
        return Response(dict)  # Return the sample dictionary for GET requests
    elif (request.method == "POST"):
        data = request.data  # Get the data from the request body
        print("POST request", data)
        return Response(data)  # Echo back the received data
    elif (request.method == "PUT"):
        print("PUT request")
        return Response(dict)  # Return the sample dictionary for PUT requests


@api_view(["GET", "POST", "PUT", "PATCH", "DELETE"])
def people(request):
    """
    CRUD operations for Person model.

    GET: Retrieves all people from the database and returns serialized data
    POST: Creates a new person record from the provided data
    PUT: Updates an existing person record completely (requires all fields)
    PATCH: Partially updates an existing person record (only specified fields)

    Returns:
        - GET: List of all people
        - POST/PUT/PATCH: Created/Updated person data or validation errors
    """
    if (request.method == "GET"):
        # dbData = Person.objects.all()  # Query to fetch all people from Database
        # Query to fetch all people from Database who have a color
        dbData = Person.objects.filter(color__isnull=False)
        # Serialize multiple objects by setting many=True
        serializer = PeopleSerializer(dbData, many=True)
        return Response(serializer.data)  # Return serialized data

    elif (request.method == "POST"):
        data = request.data  # Get the data from the request body
        # Create a new serializer instance with the received data
        serializer = PeopleSerializer(data=data)
        if (serializer.is_valid()):  # Validate the data
            serializer.save()  # Save the valid data to database
            return Response(serializer.data)  # Return the created object
        return Response(serializer.errors)  # Return validation errors if any

    elif (request.method == "PUT"):
        data = request.data  # Get the data from the request body
        id = data["id"]  # Extract the ID from the request data
        dbObj = Person.objects.get(id=id)  # Fetch the object to update
        if not dbObj:
            return Response("Not found")  # Return error if object not found
        # Create serializer with existing object and new data
        serializer = PeopleSerializer(dbObj, data=data)
        if (serializer.is_valid()):  # Validate the data
            serializer.save()  # Save the updated data
            return Response(serializer.data)  # Return the updated object
        return Response(serializer.errors)  # Return validation errors if any

    elif (request.method == "PATCH"):
        data = request.data  # Get the data from the request body
        id = data["id"]  # Extract the ID from the request data
        dbObj = Person.objects.get(id=id)  # Fetch the object to update
        if not dbObj:
            return Response("Not found")  # Return error if object not found
        # Create serializer with existing object and new data, allowing partial updates(unlike PUT, all fields need not be passed from the client)
        serializer = PeopleSerializer(dbObj, data=data, partial=True)
        if (serializer.is_valid()):  # Validate the data
            serializer.save()  # Save the updated data
            return Response(serializer.data)  # Return the updated object
        return Response(serializer.errors)  # Return validation errors if any

    elif (request.method == "DELETE"):
        id = request.query_params.get("id")
        dbObj = Person.objects.get(id=id)
        if not dbObj:
            return Response("Not found")
        dbObj.delete()
        return Response("Deleted")


@api_view(["POST"])
def login(request):
    data = request.data
    serializer = LoginSerializer(data=data)
    if serializer.is_valid():
        print(serializer.validated_data)
        return Response(serializer.data)
    return Response(serializer.errors)


# These 4 are the same as the people function in the index view which handles GET, POST, PUT, PATCH, DELETE requests manually
class PeopleAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        print(request.user)
        return Response({"message": "GET request"})

    def post(self, request):
        return Response({"message": "POST request"})

    def patch(self, request):
        return Response({"message": "PATCH request"})

    def put(self, request):
        return Response({"message": "PUT request"})

    def delete(self, request):
        return Response({"message": "DELETE request"})


# These 3 are the same as the people function in the index view which handles GET, POST, PUT, PATCH, DELETE requests automatically
class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()

    def list(self, request):
        user_query = request.query_params.get("name")
        queryset = self.queryset
        if user_query:
            queryset = queryset.filter(name__startswith=user_query)
        serializer = PeopleSerializer(queryset, many=True)
        return Response(serializer.data)
