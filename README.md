# Django REST Framework Demo Project

This project demonstrates various Django REST Framework (DRF) concepts and best practices, serving as a comprehensive reference for building RESTful APIs with Django.

## Project Overview

This application showcases different approaches to building APIs in Django, from function-based views to class-based views and viewsets. It includes:

- Authentication using Token Authentication
- Serialization of data
- Validation at multiple levels
- Various view implementations
- Model relationships
- Custom actions and endpoints

## Models

The project includes two main models:

1. **Person**: Represents individuals with name, age attributes and an optional relationship to a Color
2. **Color**: Represents color information with a color_name field

```python
class Color(models.Model):
    color_name = models.CharField(max_length=200)

class Person(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    color = models.ForeignKey(Color, null=True, blank=True, on_delete=models.CASCADE)
```

## Serializers

The project demonstrates various serialization techniques:

### Basic Serializer (non-model)

```python
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
```

### Model Serializer with Validation

```python
class PeopleSerializer(serializers.ModelSerializer):
    color = ColorSerializer(read_only=True)  # Nested serialization
    color_id = serializers.PrimaryKeyRelatedField(
        queryset=Color.objects.all(), source='color', write_only=True
    ) 
    color_info = serializers.SerializerMethodField()  # Custom field
    
    class Meta:
        model = Person
        fields = "__all__"
    
    # Custom method field
    def get_color_info(self, obj):
        color_obj = Color.objects.get(id=obj.color.id)
        return {
            "color_name": color_obj.color_name,
            "hex_code": "#24dcdb"
        }
        
    # Object-level validation
    def validate(self, data):
        if data.get("age") and data["age"] < 18:
            raise serializers.ValidationError("Age cannot be less than 18")
        return data
        
    # Field-level validation
    def validate_age(self, value):
        if value and value < 18:
            raise serializers.ValidationError("Age cannot be less than 18")
        return value
```

## API Endpoints & View Types

### Function-Based Views

Simple API views implemented as functions with the `@api_view` decorator:

```python
@api_view(["GET", "POST", "PUT", "PATCH", "DELETE"])
def people(request):
    # CRUD operations for the Person model
    # ...
```

### Class-Based Views (APIView)

Object-oriented approach to API views with methods mapped to HTTP methods:

```python
class PeopleAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get(self, request):
        # Handle GET requests
        # ...
        
    def post(self, request):
        # Handle POST requests
        # ...
```

### ViewSets

A higher-level abstraction that combines CRUD operations into a single class:

```python
class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()
    http_method_names = ["get", "post"]  # Limit available methods
    
    # Custom action
    @action(detail=True, methods=["POST"])
    def send_email(self, request, pk=None):
        # Custom endpoint functionality
        # ...
```

## Authentication & Permission

The project implements:

1. **Token Authentication**: Using Django REST Framework's TokenAuthentication
2. **Registration**: Custom user registration view
3. **Login**: Custom login view that returns an authentication token

```python
class LoginAPI(APIView):
    def post(self, request):
        # Authenticate user and return token
        # ...
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)
```

## Advanced Features

### Filtering & Pagination

The project demonstrates:
- QuerySet filtering using request parameters
- Pagination of results

```python
def list(self, request):
    user_query = request.query_params.get("name")
    queryset = self.queryset
    if user_query:
        queryset = queryset.filter(name__startswith=user_query)
    # ...
```

### Custom Actions

Adding non-standard endpoints to ViewSets:

```python
@action(detail=True, methods=["POST"])
def send_email(self, request, pk=None):
    # Custom functionality for a specific resource
    # ...
```

## URL Routing

The project demonstrates multiple URL routing patterns:

1. **Direct function mappings**: `path("person/", people)`
2. **Class-based view mappings**: `path("people-route/", PeopleAPI.as_view())`
3. **ViewSet routing using DefaultRouter**: 
   ```python
   router = DefaultRouter()
   router.register(r"people-viewset", PeopleViewSet, basename="people-viewset")
   path("", include(router.urls))
   ```

## Key Concepts Demonstrated

1. **Serialization**: Converting complex data types to Python native data types and then to JSON
2. **Deserialization**: Converting JSON to Python native data types and then to complex data types
3. **Validation**: Field-level, object-level validation in serializers
4. **Authentication**: Token-based authentication
5. **Authorization**: Permission classes to restrict access
6. **ViewSets & Routers**: High-level API building abstractions
7. **Filtering & Pagination**: Managing large datasets
8. **Custom Actions**: Extending the REST framework for specialized operations
9. **Nested Serializers**: Handling related models in API responses

## Running the Project

1. Clone the repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment: 
   - Windows: `.venv\Scripts\activate`
   - Unix/MacOS: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Start the development server: `python manage.py runserver`

## API Endpoints

- `api/register/` - User registration
- `api/login/` - User login (returns auth token)
- `api/index/` - Simple test endpoint
- `api/person/` - CRUD operations for Person model (function-based)
- `api/people-route/` - Person API (class-based)
- `api/people-viewset/` - Person API (ViewSet)
- `api/people-viewset/{id}/send_email/` - Custom action example 