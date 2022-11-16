from rest_framework import serializers
from .models import Todo, Category
from pprint import pprint

#-------Model ViewSet Ex------, ORDER MATTERS regarding nesting#
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__" 

class TodoSerializer(serializers.ModelSerializer):
    category = CategorySerializer() #we can nest a serializer within this one, to get all info on the front end
    class Meta:
        model = Todo
        fields = "__all__" #can use a tuple to specify

    def create(self, validated_data): #overwrite the create method inherited from ModelSerializer class, pass in self since instance of it
        pprint(validated_data) #validated data has been converted to python
        category = validated_data.pop('category')
        cat_instance = Category.objects.get(name=category['name'])
        todo = Todo.objects.create(**validated_data, category=cat_instance) #destructuring the object and passing in as kwargs 
        return todo

