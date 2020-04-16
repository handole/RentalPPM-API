from django.http import Http404,HttpResponse
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User, Group, Permission
from api.models import receiving_header, receiving_detail, rental_stock_card, rental_stock_sn, \
    stock_sn_history, master_item, rental_header, rental_order_header, invoice_header, master_customer, \
    master_location, rental_order_detail, rental_detail,master_user,invoice_detail
from api.models.master_employee import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.dispatch import receiver, Signal
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from api.serializers import NestedReceivingHeaderWriteSerializer, NestedReceivingHeaderReadSerializer, \
    NestedStockCardSerializer, NestedRentalHeaderReadSerializer, NestedRentalHeaderWriteSerializer, \
    NestedRentalOrderHeaderWriteSerializer, NestedRentalOrderHeaderReadSerializer, RentalStockSNSerializer, \
    StockSNHistorySerializer, ItemReadSerializer,NestedInvoiceReadSerializer,NestedInvoiceReadSerializerNew,NestedInvoiceSerializer,\
    NestedReadRentalDetail,InvoiceDetailSerializer,GroupSerializer,GroupPermission,NestedMasterItemReadSerializer,\
    NestedStockSNHistorySerializer
import datetime
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum,Count
from api.models.rental_register_detail import rental_detail_sn
from django.db.models import Q


# This view is purposely used for testing only, improvement is considered and might used in further development

update_on_nested_serializer = Signal(providing_args=['test'])  # custom signal
update_on_rental_register = Signal(providing_args=['test'])  # custom signal 2
update_on_rental_order = Signal(providing_args=['test'])  # custom signal 3
todaysDate = datetime.datetime.today().strftime('%Y-%m-%d')  # get current date


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

# Rental Register
class NestedRentalRegister(APIView):
    def get(self, request, format=None):
        rentalHeader = rental_header.objects.all()
        serializers = NestedRentalHeaderReadSerializer(rentalHeader, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        # request.data['number'] = getDocumentNumber(2)  # get document number for this request
        request.data['counter'] = getCounter(2)  # get counter for this request
        serializers = NestedRentalHeaderWriteSerializer(data=request.data)
        if serializers.is_valid():        
            ids=serializers.save()            
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class NestedKembaliRentalRegister(APIView):
    def get(self, request, format=None):
        rentalHeader = rental_header.objects.filter(Q(status="APPROVED") | Q(status="LUNAS"))
        # rentalHeader = rental_header.objects.filter(status="APPROVED")
        serializers = NestedRentalHeaderReadSerializer(rentalHeader, many=True)
        return Response(serializers.data)    


@api_view(['GET'])
def getAllRentalOrderApproved(request):
    rentalOrderHeader = rental_order_header.objects.filter(status="APPROVED")
    serializers = NestedRentalOrderHeaderReadSerializer(rentalOrderHeader, many=True)
    return Response(serializers.data)


# Rental Register Details
class NestedRentalRegisterDetails(APIView):
    def get_object(self, pk):
        try:
            return rental_header.objects.get(pk=pk)
        except rental_header.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        rentalHeader = self.get_object(pk)
        serializers = NestedRentalHeaderReadSerializer(rentalHeader)
        snhistoryIncoming = stock_sn_history.objects.filter(IncomingRef_id=pk)
        snhistoryRental = stock_sn_history.objects.filter(RentalRef_id=pk)
        if snhistoryRental.count() > 0:
            SNSHistory = StockSNHistorySerializer(snhistoryRental, many=True)
            newDict = serializers.data
            newDict['SNS'] = SNSHistory.data
            return Response(newDict)
        elif snhistoryIncoming.count() > 0:
            SNSHistory = StockSNHistorySerializer(snhistoryIncoming, many=True)
            newDict = serializers.data
            newDict['SNS'] = SNSHistory.data
            return Response(newDict)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        rentalHeader = self.get_object(pk)
        sns = request.data.pop("SNS", None)
        now = datetime.datetime.today().strftime('%Y-%m-%d')
        rentalHeaderId = pk
        pay_type = request.data['pay_type']
        if request.data['status'] == "APPROVED":        
            for sn in sns:
                 if sn['stock_code_id'] == None:
                    pass
                 elif sn['stock_code_id'] != None:
                    print(sn['stock_code_id'])
                    targetedRental = rental_stock_sn.objects.get(pk=sn['stock_code_id'])
                    targetedRental.status = "KELUAR"
                    targetedRental.save()
                    stock_sn_history.objects.create(
                        date=now,
                        status="KELUAR",
                        RentalRef_id=rental_header(pk),
                        stock_code_id=rental_stock_sn(sn['stock_code_id'])
                    )
        elif request.data['status'] == "KEMBALI RENTAL":
            for sn in sns:
                # print(sn['stock_code_id'])
                targetedRental = rental_stock_sn.objects.get(pk=sn['old_stock_code_id'])
                targetedRental.status = "MASUK"
                targetedRental.save()
                stock_sn_history.objects.create(
                    date=now,
                    status="MASUK",
                    RentalRef_id=rental_header(pk),
                    stock_code_id=rental_stock_sn(sn['old_stock_code_id'])
                )
                targetedRental = rental_stock_sn.objects.get(pk=sn['new_stock_code_id'])
                targetedRental.status = "KELUAR"
                targetedRental.save()
                stock_sn_history.objects.create(
                    date=now,
                    status="KELUAR",
                    RentalRef_id=rental_header(pk),
                    stock_code_id=rental_stock_sn(sn['new_stock_code_id'])
                )
            rentaldetailheader = request.data["RentalDetailHeader"]            
            for rental in rentaldetailheader:
                now_masteritem = rental_detail.objects.filter(rental_header_id_id=pk).values('master_item_id')[0]['master_item_id']
                if rental['master_item_id'] == now_masteritem:                    
                    rdsn = rental['RDSN']
                    for rd in rdsn:
                        rental_detail_sn.objects.filter(rental_detail_sn_id=rd['rental_detail_sn_id']).update(stock_code_id_id=rd['stock_code_id'])
                else:
                    rdsn = rental['RDSN']
                    for rd in rdsn:
                        rental_detail_sn.objects.filter(rental_detail_sn_id=rd['rental_detail_sn_id']).update(stock_code_id_id=rd['stock_code_id'])
        elif request.data['status'] == "SELESAI":
            for sn in sns:
                print(sn['stock_code_id'])
                targetedRental = rental_stock_sn.objects.get(pk=sn['stock_code_id'])
                targetedRental.status = "MASUK"
                targetedRental.save()
                stock_sn_history.objects.create(
                    date=now,
                    status="MASUK",
                    RentalRef_id=rental_header(pk),
                    stock_code_id=rental_stock_sn(sn['stock_code_id'])
                )
        serializers = NestedRentalHeaderWriteSerializer(rentalHeader, data=request.data)        
        if serializers.is_valid():
            if request.data['status'] == "APPROVED" and request.user.is_superuser == True:
                serializers.save()
                if pay_type == 1:
                    rental_header.objects.filter(rental_header_id=pk).update(status="LUNAS")
                    timeNow = datetime.datetime.now().strftime('%Y-%m-%d')
                    invoice_header.objects.create(date=timeNow,
                                              amount=request.data['amount'],
                                              customer=request.data['customer_id'],
                                              pay_method=request.data['pay_method'],
                                              status="LUNAS",
                                              rental_header_id=rentalHeader)
                elif pay_type == 2:
                    rental_header.objects.filter(rental_header_id=pk).update(status="APPROVED")
                    timeNow = datetime.datetime.now().strftime('%Y-%m-%d')
                    invoice_header.objects.create(date=timeNow,
                                              amount=request.data['amount'],
                                              customer=request.data['customer_id'],
                                              pay_method=request.data['pay_method'],
                                              status="SEDANG BERJALAN",
                                              rental_header_id=rentalHeader)
                # update_on_rental_register.send(sender=rental_header, test=serializers.data)
                return Response(serializers.data, status=status.HTTP_200_OK)
            elif request.data['status'] == "DRAFT":
                serializers.save()
                update_on_rental_register.send(sender=rental_header, test=serializers.data)
                return Response(serializers.data, status=status.HTTP_200_OK)
            elif request.data['status'] == "KEMBALI RENTAL" and request.user.is_active == True:
                serializers.save()
                rental_header.objects.filter(rental_header_id=pk).update(status="APPROVED")
                return Response(serializers.data,status=status.HTTP_200_OK)
            elif request.data['status'] == "SELESAI" and request.user.is_active == True:
                serializers.save()
                rental_header.objects.filter(rental_header_id=pk).update(status="SELESAI")
                return Response(serializers.data,status=status.HTTP_200_OK)
            elif request.data['status'] == "APPROVED" and request.user.is_active == False:
                return Response("Access Denied", status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


# This view is used to get and post object of incoming management module
class NestedReceivingManagement(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        headers = receiving_header.objects.all()
        serializers = NestedReceivingHeaderReadSerializer(headers, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        # request.data['number'] = getDocumentNumber(3)  # get document number for this request
        # request.data['counter'] = getCounter(3)  # get counter for this request
        request.data['date'] = datetime.datetime.today().strftime('%Y-%m-%d')

        serializers = NestedReceivingHeaderWriteSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

# This view is use to get and update specific object of incoming management module
class NestedReceivingManagementDetails(APIView):
    def get_object(self, pk):
        try:
            return receiving_header.objects.get(pk=pk)
        except receiving_header.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        header = self.get_object(pk)
        serializer = NestedReceivingHeaderReadSerializer(header)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        header = self.get_object(pk)
        if request.data['status'] == "APPROVED":
            request.data['approval1_date'] = datetime.datetime.today().strftime('%Y-%m-%d')
        serializer = NestedReceivingHeaderWriteSerializer(header, data=request.data)
        if serializer.is_valid():
            if request.data['status'] == "APPROVED" and request.user.is_active == True:
                serializer.save()
                update_on_nested_serializer.send(sender=receiving_header, test=serializer.data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif request.data['status'] == "DRAFT":
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif request.data['status'] == "APPROVED" and request.user.is_active == False:
                return Response("Access Denied", status=status.HTTP_401_UNAUTHORIZED)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Rental Order Management
class NestedRentalOrderManagement(APIView):
    def get(self, request, format=None):
        rentalOrderHeader = rental_order_header.objects.all()
        serializer = NestedRentalOrderHeaderReadSerializer(rentalOrderHeader, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # request.data['number'] = getDocumentNumber(1)  # get document number for this request
        request.data['counter'] = getCounter(1)  # get counter for this request

        serializers = NestedRentalOrderHeaderWriteSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


# Rental Order Management Details
class NestedRentalOrderManagementDetails(APIView):
    def get_object(self, pk):
        try:
            return rental_order_header.objects.get(pk=pk)
        except rental_order_header.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        rentalOrderHeader = self.get_object(pk)
        serializers = NestedRentalOrderHeaderReadSerializer(rentalOrderHeader)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        rentalOrderHeader = self.get_object(pk)
        serializers = NestedRentalOrderHeaderWriteSerializer(rentalOrderHeader, data=request.data)
        if serializers.is_valid():
            if request.data['status'] == "APPROVED" and request.user.is_active == True:
                serializers.save()
                update_on_rental_order.send(sender=rental_order_header, test=serializers.data)
                return Response(serializers.data, status=status.HTTP_200_OK)
            elif request.data['status'] == "DRAFT" and request.user.is_active == True:
                serializers.save()
                return Response(serializers.data, status=status.HTTP_200_OK)                
            elif request.data['status'] == "APPROVED" and request.user.is_active == False:
                return Response("Access denied", status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@receiver(update_on_rental_order)
def addToRentalRegister(sender, **kwargs):
    dataRental = kwargs['test']

    if dataRental['status'] == "APPROVED":
        timeNow = datetime.datetime.now().strftime('%Y-%m-%d')
        numberRR = getDocumentNumber(2)
        counterRR = getCounter(2)

        # print(dataRental)

        rentalHeader = rental_header.objects.create(
            date=timeNow,
            number=numberRR,
            number_prefix="",
            counter=counterRR,
            tax=dataRental['tax'],
            discount_type=dataRental['discount_type'],
            discount=dataRental['discount'],
            delivery_cost=dataRental['delivery_fee'],
            amount=dataRental['amount'],
            notes=dataRental['notes'],
            salesman=dataRental['salesman'],
            notes_kwitansi="",
            status="DRAFT",
            rental_start_date=dataRental['rental_start_date'],
            rental_end_date=dataRental['rental_end_date'],
            sales_order_id=rental_order_header(dataRental['sales_order_id']),
            customer_id=master_customer(dataRental['customer_id']),
            location_id=master_location(dataRental['location_id']),
            approved_by=dataRental['approved_by'],
            approved_date=dataRental['approved_date'],
            pay_type=1,
            pay_method=1,
            note_kwitansi=dataRental['notes_kwitansi']
        )

        RODHeader = dataRental.pop('RODHeader', None)

        for x in RODHeader:
            rental_detail.objects.create(
                price=x['price'],
                qty=x['qty'],
                discount_type=x['discount_type'],
                discount_method=x['discount_method'],
                total=x['total'],
                rental_header_id=rentalHeader,
                order_detail_id=rental_order_detail(x['order_detail_id']),
                master_item_id=master_item(x['master_item_id'])
            )


@api_view(['GET', 'POST'])
def extendRental(request):
    # request.data['number'] = getDocumentNumber(2)
    request.data['counter'] = getCounter(2)
    request.data['status'] = "DRAFT"
    request.data['date'] = datetime.datetime.today().strftime('%Y-%m-%d')
    # request.data['user_id'] = request.user
    serializers = NestedRentalHeaderWriteSerializer(data=request.data)
    if serializers.is_valid():
        ids=serializers.save()
        return Response(serializers.data, status=status.HTTP_201_CREATED)
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

