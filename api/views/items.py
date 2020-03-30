from django.http import Http404,HttpResponse
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User, Group, Permission
from api.models import master_item, rental_stock_sn, rental_stock_card
from api.models.master_employee import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.dispatch import receiver, Signal
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from api.serializers import NestedReceivingHeaderReadSerializer, NestedStockCardSerializer, \
    RentalStockSNSerializer, StockSNHistorySerializer, NestedReadRentalDetail, NestedMasterItemReadSerializer,\
    NestedStockSNHistorySerializer, ItemReadSerializer
import datetime
from django.db.models import Sum,Count
from api.models.rental_register_detail import rental_detail_sn
from django.db.models import Q

# This view is purposely used for testing only, improvement is considered and might used in further development

update_on_nested_serializer = Signal(providing_args=['test'])  # custom signal
update_on_rental_register = Signal(providing_args=['test'])  # custom signal 2
update_on_rental_order = Signal(providing_args=['test'])  # custom signal 3
todaysDate = datetime.datetime.today().strftime('%Y-%m-%d')  # get current date


def getDocumentNumber(r):
    now = datetime.datetime.now()
    docNumb = ""
    if r == 1:
        # This is for Rental Order Management
        docNumb += "RO/"
        query = rental_order_header.objects.count()
        if query < 1:
            docNumb += "0001"
        else:
            query2 = rental_order_header.objects.all().order_by('-counter')[:1].get()
            j = query2.counter + 1
            docNumb += str(j).zfill(4)
    elif r == 2:
        # This is for Rental Register
        docNumb += "RN/"
        query = rental_header.objects.count()
        if query < 1:
            docNumb += "0001"
        else:
            query2 = rental_header.objects.all().order_by('-counter')[:1].get()
            j = query2.counter + 1
            docNumb += str(j).zfill(4)
    elif r == 3:
        # This is for Incoming or Receiving Management
        docNumb += "IN/"
        query = receiving_header.objects.count()
        if query < 1:
            docNumb += "0001"
        else:
            query2 = receiving_header.objects.all().order_by('-counter')[:1].get()
            j = query2.counter + 1
            docNumb += str(j).zfill(4)
    docNumb += "/" + now.strftime("%m") + "/" + now.strftime("%Y")
    return docNumb


def getCounter(r):
    c = ""
    if r == 1:
        query = rental_order_header.objects.count()
        if query < 1:
            c += "1"
        else:
            query2 = rental_order_header.objects.all().order_by('-counter')[:1].get()
            c += str(query2.counter + 1)
    elif r == 2:
        query = rental_header.objects.count()
        if query < 1:
            c += "1"
        else:
            query2 = rental_header.objects.all().order_by('-counter')[:1].get()
            c += str(query2.counter + 1)
    elif r == 3:
        query = receiving_header.objects.count()
        if query < 1:
            c += "1"
        else:
            query2 = receiving_header.objects.all().order_by('-counter')[:1].get()
            c += str(query2.counter + 1)
    return c

class getPriceMasterItem(APIView):
    def post(self, request, format=None):
        r_header = request.data['rental_header_id']
        stockmanagement = rental_detail.objects.filter(rental_header_id_id=r_header)
        serializers = NestedReadRentalDetail(stockmanagement, many=True)
        return Response(serializers.data)
        # return Response(stockmanagement)

@api_view(['GET'])
def getItemByCategory(request, b=1):
    item = master_item.objects.filter(master_group_id=b)
    serializer = ItemReadSerializer(item, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getItemByBarcode(request, b=1):
    item = master_item.objects.filter(barcode=b)
    serializer = ItemReadSerializer(item, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getItemSNs(request, i=1):
    sns = rental_stock_sn.objects.filter(stock_card_id__in=(rental_stock_card.objects.filter(item_master_id=i)))
    serializers = RentalStockSNSerializer(sns, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getItemSNsAvailable(request, i=1):
    sns = rental_stock_sn.objects.filter(stock_card_id__in=(rental_stock_card.objects.filter(item_master_id=i))).filter(
        status="MASUK")
    serializers = RentalStockSNSerializer(sns, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getUnapprovedHeader(request, s=1):
    incomingHeader = receiving_header.objects.filter(status=s)
    serializers = NestedReceivingHeaderReadSerializer(incomingHeader, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getDistinctItem(request):
    stocks = rental_stock_card.objects.distinct('item_master_id')
    serializers = NestedStockCardSerializer(stocks, many=True)

    a = serializers.data

    for x in a:
        SNSQty = rental_stock_sn.objects.filter(
            stock_card_id__in=(rental_stock_card.objects.filter(item_master_id=x['item_master_id']))).filter(
            status="MASUK").count()
        x['qty'] = SNSQty

    # return Response(serializers.data, status=status.HTTP_200_OK)
    return Response(a, status=status.HTTP_200_OK)



class NestedMasterItem(APIView):
    def get(self, request, format=None):
        masteritem = master_item.objects.all()
        serializers = NestedMasterItemReadSerializer(masteritem, many=True)
        return Response(serializers.data)

class NestedMasterItemDetails(APIView):
    def get_object(self, pk):
        try:
            return master_item.objects.get(pk=pk)
        except master_item.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        header = self.get_object(pk)
        serializer = NestedMasterItemReadSerializer(header)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        header = self.get_object(pk)
        serializer = NestedMasterItemReadSerializer(header, data=request.data)
        if serializer.is_valid():            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# This view is used to get rental stock card, rental stock sn, and stock sn history
class NestedStockManagementDetails(APIView):
    def get_object(selfs, pk):
        try:
            return rental_stock_card.objects.get(pk=pk)
        except receiving_header.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        header = self.get_object(pk)
        serializer = NestedStockCardSerializer(header)
        return Response(serializer.data)

