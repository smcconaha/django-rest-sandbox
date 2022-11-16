from django.shortcuts import render
from django.http.response import Http404 #means we potentuially set up a not found route if thing trying to get not found
from rest_framework.views import APIView #gives us get, post methods and other things
from .models import Todo #importing todo model
from .serializers import TodoSerializer #importing our serializer
from rest_framework.response import Response
from rest_framework import status

class TodoAPIView(APIView): #meaning it inherits from the APIView, gives us functions and methods that we can override
#---Single todo read op, with GET we query db and use serializer to convert to JSON
    def get_object(self, pk): #when we define method on class we pass in self and PK for thing we are searching for
        try:
            return Todo.objects.get(pk=pk) #pk or id equals primary key that we are passing in
        except Todo.DoesNotExist: #if we dont get one
            raise Http404 #raise exception that we imported
#---All todo read op
    def get(self, request, pk=None, format=None):
        if pk: #if its being passed in
            data = self.get_object(pk) #this method is called on line 10 and passing pk in
            serializer = TodoSerializer(data) #grab object from the db and serialize the data based on method defined
        else:
            data = Todo.objects.all() #ORM tool for querying whole db, can use orderby here too
            serializer = TodoSerializer(data, many=True) #expecting more than one result, another keyword argument. DEFAULTS to false

        return Response(serializer.data) #response coming from rest framework and in response we want to use serializer defined above and specifically the part with data on it

#---Post, overriding from the parent - we send JSON over and have to deserialize it into something DB understands
    def post(self, request, format=None):
        print('YOU SENT A POST REQUEST!')
        data = request.data
        serializer = TodoSerializer(data=data)#takes data coming in and change from JSON into something Python can understand
    #check if data is valid
        if serializer.is_valid(raise_exception=True):
    #if valid we continue on, here is where we would save
            serializer.save()

    #inform front end that save was successful or result
            response = Response()#another instance of class built up in rest framework
            response.data = { #building up the response
                'message': 'Todo Created Successfully',
                'data': serializer.data,
            }
            return response
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Two more methods 
# put() meaning update what I am sending or create a new one and patch() says I know which one I want to update

#---Put where we can update something like switching todos from not complete to compete
    def put(self, request, pk=None, format=None): #format is keyword argument, it needs this, with pk = none we can use that to get a single one
        print('UPDATE!')
        todo_to_update = Todo.objects.get(pk=pk) #we got what it looks lke in the db
        data = request.data
        serializer = TodoSerializer(instance=todo_to_update, data=data, partial=True) #instance that we want to update and pass in is one we just created.  We also need to send over new info from request for updating, partial meaning updating part of data

        serializer.is_valid(raise_exception=True) #checking for validity and raising exception if not
        serializer.save()

        response = Response() #build up response

        response.data = {
            'message': 'Todo Updated Successfully',
            'data': serializer.data
        }

        return response

    def delete(self, request, pk, format=None):
        print('DELETED SUCKA!')
        todo_delete = Todo.objects.get(pk=pk) #we got what it looks lke in the db
        data = request.data
        todo_delete.delete()
        response = Response(status=status.HTTP_204_NO_CONTENT)
        return response