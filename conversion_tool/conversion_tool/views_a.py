from django.shortcuts import render
from rest_framework.schemas import SchemaGenerator
from rest_framework.permissions import AllowAny
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
import hla
import conversion_functions
from conversion_functions import convert_allele_to_ag
from hla import allele_truncate
from . import serializers
from rest_framework_swagger.views import get_swagger_view







class AlleleApiView(generics.GenericAPIView):
    """Returns antigen for an allele"""
    serializer_class = serializers.AlleleSerializer
    permission_classes = [AllowAny,]
    
    #def get(self, request):
        #generator = SchemaGenerator()
        #schema = generator.get_schema(request=request)
        #obj = ["UNOS antigen mapping for WHO HLA alleles"]
        #return Response(obj)

    def post(self, request, format=None):
        """Returns UNOS antigen for an allele."""
        """parameters: 
        allele:string
        """
        serializer = serializers.AlleleSerializer(data=request.data)    

        if serializer.is_valid(raise_exception=True):
            
            #serializer.create(allele)
            #allele = serializer.save()
            #serializer.create()
            allele = serializer.data.get('allele')
            ag = conversion_functions.convert_allele_to_ag(allele)
            result = {'Antigen': ag}
            return Response(result,  status=status.HTTP_200_OK)
        else:
            return Response({"Error": "Check if allele is IMGT/HLA"}, status=status.HTTP_400_BAD_REQUEST)
            #serializer.errors, status=status.HTTP_400_BAD_REQUEST)    