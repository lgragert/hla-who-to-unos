from django.shortcuts import render
from rest_framework.schemas import SchemaGenerator
from rest_framework.permissions import AllowAny
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
import hla
import reverse_conversion
from reverse_conversion import map_single_ag_to_alleles
from hla import allele_truncate
from . import serializers
from rest_framework_swagger.views import get_swagger_view







class AlleleMappingApiView(generics.GenericAPIView):
    """Returns list of IMGT/HLA alleles for UNOS antigen entered"""
    serializer_class = serializers.AlleleMappingSerializer
    permission_classes = [AllowAny,]
    
    #def get(self, request):
        #generator = SchemaGenerator()
        #schema = generator.get_schema(request=request)
        #obj = ["UNOS antigen mapping for WHO HLA alleles"]
        #return Response(obj)

    def post(self, request, format=None):
        """Returns IMGT/HLA alleles list for UNOS antigen."""
        """parameters: 
        antigen:string
        """
        serializer = serializers.AlleleMappingSerializer(data=request.data)    

        if serializer.is_valid(raise_exception=True):
            
            #serializer.create(allele)
            #allele = serializer.save()
            #serializer.create()
            antigen = serializer.data.get('antigen')
            allele_list = reverse_conversion.map_single_ag_to_alleles(antigen)
            result = {'IMGT/HLA_alleles_list': allele_list}
            return Response(result,  status=status.HTTP_200_OK)
        else:
            return Response({"Error": "Check if it's UNOS antigen"}, status=status.HTTP_400_BAD_REQUEST)
            #serializer.errors, status=status.HTTP_400_BAD_REQUEST)    