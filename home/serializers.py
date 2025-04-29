from rest_framework import serializers
from .models import Person, Color


# we use serializer.Serializer to create a serializer for a custom request (login) where we don't have a model
# we can use serializer.ModelSerializer to create a serializer for a model when we have a model
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ["color_name"]


class PeopleSerializer(serializers.ModelSerializer):
    # instead of using depth, we can use a serializer for the related model to include  only the required related model data in the response (color).
    # example: get only the color name in the response
    color = ColorSerializer() # serializing foreign table data
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
        return data
    # field specific validation (this will override the object level validation)

    def validate_age(self, value):
        if value and value < 18:
            raise serializers.ValidationError(
                "Age cannot be less than 18 in field level validation")
        return value
