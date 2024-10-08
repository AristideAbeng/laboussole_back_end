from django.shortcuts import render, get_object_or_404
from .models import Actualit
from . import serializers
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from django.db.models import Q, Sum, Case, When, Value, IntegerField
from django.db.models.functions import Length

# Create your views here.

class ActualitListView(generics.GenericAPIView):

    serializer_class = serializers.ActualitCreationSerializer

    queryset = Actualit.objects.all()

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Actualit.objects.all()

        # Get the sender_id from request query parameters
        sender_id = self.request.query_params.get('sender_id', None)
        if sender_id:
            queryset = queryset.filter(sender_id=sender_id)
        
        search_query = self.request.query_params.get('search', None)
        if search_query:
            search_words = search_query.split()
            conditions = Q()
            for word in search_words:
                conditions |= Q(titre__unaccent__icontains=word)
            queryset = queryset.filter(conditions)
            queryset = queryset.annotate(
                word_count=Sum(
                    Case(
                        *[When(titre__unaccent__icontains=word, then=Value(1)) for word in search_words],
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                )
            )
            queryset = queryset.order_by('-word_count', 'titre')
        else:
            queryset = queryset.order_by('titre')
        
        return queryset
    def get(self,request):

        queryset = self.get_queryset()
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.serializer_class(instance=queryset,many=True)

        return Response(data=serializer.data,status=status.HTTP_200_OK)


    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        user = request.user

        # Check if the authenticated user is an admin
        if not user.is_staff:
            return Response({"error": "Only admin users can perform this action"}, status=status.HTTP_403_FORBIDDEN)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActualitDetailView(generics.GenericAPIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = serializers.ActualitCreationSerializer

    def get(self,request,Actualit_id):

        actualite = get_object_or_404(Actualit,pk=Actualit_id)

        serializer = self.serializer_class(instance=actualite)

        return Response(data=serializer.data,status=status.HTTP_200_OK)


    def put(self, request, actualit_id):
        # Check if the authenticated user is an admin
        if not request.user.is_staff:
            return Response({"error": "Only admin users can perform this action"}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        actualite = get_object_or_404(Actualit, pk=actualit_id)
        serializer = self.serializer_class(data=data, instance=actualite)
        
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, actualit_id):
        # Check if the authenticated user is an admin
        if not request.user.is_staff:
            return Response({"error": "Only admin users can perform this action"}, status=status.HTTP_403_FORBIDDEN)
        
        actualite = get_object_or_404(Actualit, pk=actualit_id)
        actualite.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

