from rest_framework import serializers
from .models import Person, Color
from django.contrib.auth.models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        if (data["username"]):
            if (User.objects.filter(username=data["username"]).exists()):
                raise serializers.ValidationError("username is already taken")
        if (data["email"]):
            if (User.objects.filter(email=data["email"]).exists()):
                raise serializers.ValidationError("email is already taken")
        return data 
    
    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create(username = validated_data["username"], email = validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return validated_data
# we use serializer.Serializer to create a serializer for a custom request (login) where we don't have a model
# we can use serializer.ModelSerializer to create a serializer for a model when we have a model





class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ["color_name"]


class PeopleSerializer(serializers.ModelSerializer):
    # instead of using depth, we can use a serializer for the related model to include  only the required related model data in the response (color).
    # example: get only the color name in the response
    color = ColorSerializer(read_only=True)  # for reading nested data
    color_id = serializers.PrimaryKeyRelatedField(queryset=Color.objects.all(
    ), source='color', write_only=True)  # for writing with ID
    color_info = serializers.SerializerMethodField()

    class Meta:
        model = Person
        # fields = ["name", "age"]
        # exclude = ["name"]
        fields = "__all__"
        # depth = 1 # to include the related model data in the response (color)

    # custom field to include the color name and hex code in the response where hex code is not a field in the color model
    def get_color_info(self, obj):
        color_obj = Color.objects.get(id=obj.color.id)
        return {
            "color_name": color_obj.color_name,
            "hex_code": "#24dcdb"
        }

    # object level validation
    def validate(self, data):
        if data.get("age") and data["age"] < 18:
            raise serializers.ValidationError(
                "Age cannot be less than 18 in object level validation")
        # check if already exists   
        if data.get("name") and Person.objects.filter(name=data["name"]).exists():
            raise serializers.ValidationError("Name already exists")
        if data.get("email") and Person.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError("Email already exists")
        return data
    # field specific validation (this will override the object level validation)

    def validate_age(self, value):
        if value and value < 18:
            raise serializers.ValidationError(
                "Age cannot be less than 18 in field level validation")
        return value
