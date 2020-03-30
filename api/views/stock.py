from django.http import Http404, HttpResponse
from rest_framework.decorators import api_view
from api.models import master_item, rental_stock_sn, rental_stock_card
from api.models.master_employee import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.dispatch import receiver, Signal
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from api.serializers import NestedStockCardSerializer, NestedStockSNHistorySerializer, StockSNHistorySerializer
import datetime
from django.db.models import Sum, Count
from api.models.rental_register_detail import rental_detail_sn
from django.db.models import Q

update_on_nested_serializer = Signal(providing_args=['test'])  # custom signal
update_on_rental_register = Signal(providing_args=['test'])  # custom signal 2
update_on_rental_order = Signal(providing_args=['test'])  # custom signal 3
todaysDate = datetime.datetime.today().strftime('%Y-%m-%d')  # get current date

@api_view(['GET'])
def getStockHistoryBySN(request, i=1):
    SNHistory = stock_sn_history.objects.filter(stock_code_id=i)
    serializers = StockSNHistorySerializer(SNHistory, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)

# This is the receiver of signal to add new objects upon updating status in incoming module
@receiver(update_on_nested_serializer)
def addToStock(sender, **kwargs):
    ReceivingHeaderData = kwargs['test']
    Detail_from_ReceivingHeaderData = ReceivingHeaderData['RDHeader']

    if "DRAFT" == ReceivingHeaderData['status']:
        print('DRAFT, because the status is still DRAFT, so nothing happened XD')
    else:
        print('APPROVED')
        # Adding each detail in incoming module on selected header to rental stock card
        for EachDetail in Detail_from_ReceivingHeaderData:
            stockCardData = rental_stock_card.objects.create(item_master_id=EachDetail['master_item_id'],
                                                             location_id=ReceivingHeaderData['location_id'],
                                                             qty=EachDetail['qty'],
                                                             rental_header_id=None,
                                                             rental_detail_id=None,
                                                             receiving_header_id=receiving_header(
                                                                 EachDetail['receiving_header_id']),
                                                             receiving_detail_id=receiving_detail(
                                                                 EachDetail['receiving_detail_id']))
            # Check whether the object creation is success or not, if yes, put every SN in each details into
            # rental stock sn and stock sn history with status equals to 1 or available
            if stockCardData:
                # print(stockCardData)
                sn = []
                # Move all SN in RDISN of each Detail into a variable called sn, then create rental stock sn objects for each rental stock card
                for EachSNArray in EachDetail['RDISN']:
                    temp = {}
                    # print(EachSNArray)
                    for keys, values in EachSNArray.items():
                        # print("This is inside EachSNArray.items() = ", keys, values)
                        temp[keys] = values
                    sn.append(temp)
                for SN in sn:
                    stockSN = rental_stock_sn.objects.create(first_sn=SN['first_serial_number'],
                                                             new_sn=SN['new_serial_number'],
                                                             status="MASUK",
                                                             stock_card_id=stockCardData)

                    if stockSN:
                        # print("Create Rental Stock SN object success!! the ID of this object is = ", stockSN)
                        stock_sn_history.objects.create(date=todaysDate, status="MASUK",
                                                        IncomingRef_id=ReceivingHeaderData['receiving_header_id'],
                                                        stock_code_id=stockSN)
                    else:
                        print("Failed to create Rental Stock SN Object")
            else:
                print("Failed create object")

# This view is used to get and post on stock management module including
# rental stock card, rental stock sn, and stock sn history
class NestedStockManagement(APIView):
    def get(self, request, format=None):
        stockmanagement = rental_stock_card.objects.all()
        serializers = NestedStockCardSerializer(stockmanagement, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = NestedStockCardSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

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


class NestedStockSNhistory(APIView):
    def get(self, request, format=None):
        stocksnhistory = stock_sn_history.objects.all()
        serializers = NestedStockSNHistorySerializer(stocksnhistory, many=True)
        return Response(serializers.data)    