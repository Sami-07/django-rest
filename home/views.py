from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Person
from .serializers import PeopleSerializer


@api_view(["GET", "POST", "PUT", "PATCH", "DELETE"])
def index(request):
    """
    Base API endpoint that handles multiple HTTP methods.
    GET: Returns a sample dictionary with user information
    POST: Returns the received data back to the client
    PUT: Returns a sample dictionary (currently same as GET response)
    """
 
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
        dbData = Person.objects.all()  # Query to fetch all people from Database
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
    
    elif(request.method == "DELETE"):
        id = request.query_params.get("id")
        dbObj = Person.objects.get(id=id)
        if not dbObj:
            return Response("Not found")
        dbObj.delete()
        return Response("Deleted")

