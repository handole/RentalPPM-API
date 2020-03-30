from django.http import Http404,HttpResponse
from rest_framework.decorators import api_view
from api.models import invoice_header, rental_detail_sn, rental_detail, rental_stock_sn
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.dispatch import receiver, Signal
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from api.serializers import NestedInvoiceReadSerializerNew, NestedInvoiceSerializer, NestedInvoiceReadSerializer

# Invoice Management
class NestedInvoiceManagement(APIView):
    def get(self, request, format=None):    
        dataInvoice = invoice_header.objects.all().annotate(t_terbayar=Sum('InvoiceDetails__pay_amount')).order_by('invoice_header_id')
        serializer = NestedInvoiceReadSerializerNew(dataInvoice,many=True)
        #return Response(dataInvoice)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = NestedInvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NestedInvoiceManagementByID(APIView):
    def get_object(self, pk):
        try:
            return invoice_header.objects.get(pk=pk)
        except ValueError:
            raise Http404
    def get(self, request,pk, format=None):
        invoiceHeader = self.get_object(pk)
        dataInvoice = invoice_header.objects.filter(invoice_header_id=pk).annotate(t_terbayar=Sum('InvoiceDetails__pay_amount')).order_by('invoice_header_id')
        serializer = NestedInvoiceReadSerializerNew(dataInvoice,many=True)
        #return Response(dataInvoice)
        return Response(serializer.data)


class NestedInvoiceManagementDetails(APIView):
    def get_object(self, pk):
        try:
            return invoice_header.objects.get(pk=pk)
        except invoice_header.DoesNotExists:
            raise Http404

    def get(self, request, pk, format=None):
        invoiceHeader= self.get_object(pk)
        serializer = NestedInvoiceReadSerializer(invoiceHeader)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        invoiceHeader = self.get_object(pk)
        now = datetime.datetime.today().strftime('%Y-%m-%d')
        inv_header = request.data["invoice_header_id"]
        inv_detail = request.data["InvoiceDetails"]
        stat = request.data["status"]
        header_id = invoice_header.objects.filter(invoice_header_id=inv_header).values('rental_header_id_id')[0]['rental_header_id_id']
        rent_detail = rental_detail.objects.filter(rental_header_id_id=header_id)
        if stat == "BERHENTI RENTAL":
            for r in rent_detail:
                stock_codeid = rental_detail_sn.objects.filter(rental_detail_id_id=r.rental_detail_id).values('stock_code_id')[0]['stock_code_id']        
                targetedRental = rental_stock_sn.objects.get(pk=stock_codeid)
                targetedRental.status = "MASUK"
                targetedRental.save()
                stock_sn_history.objects.create(
                    date=now,
                    status="MASUK",
                    RentalRef_id=r.rental_header_id_id,
                    stock_code_id=rental_stock_sn(stock_codeid)
                )
            for i in inv_detail:
                invoice_detail.objects.create(date=now,noted=i['noted'],type_payment=i['type_payment'],
                jml_period=i['jml_period'],period=i['period'],harga_rental=i['harga_rental']
                ,pay_amount=i['pay_amount'],pay_method=i['pay_method'],invoice_header_id_id=inv_header)
            invoice_header.objects.filter(invoice_header_id=inv_header).update(status="LUNAS")
            rental_header.objects.filter(rental_header_id=header_id).update(status="LUNAS")
            return Response({"invoice_header_id":inv_header,"status":"LUNAS","InvoiceDetails":inv_detail}, status=status.HTTP_200_OK)
        if stat == "":            
            total_tagihan = int(invoice_header.objects.filter(invoice_header_id=inv_header).values('amount')[0]['amount'])
            # return HttpResponse(total_tagihan)
            for i in inv_detail:                
                t_terbayar = invoice_detail.objects.filter(invoice_header_id_id=pk).values('invoice_header_id_id').annotate(t_terbayar=Sum('pay_amount'))
                if len(t_terbayar) == 0:
                    t_terbayar = 0                    
                    total_bayar  = int(t_terbayar + int(i['pay_amount']))
                    if total_bayar < total_tagihan:                    
                        invoice_detail.objects.create(date=now,noted=i['noted'],type_payment=i['type_payment'],
                        pay_amount=i['pay_amount'],pay_method=i['pay_method'],invoice_header_id_id=inv_header)
                        return Response({"pesan":"Tagihan Terbayar","invoice_header_id":inv_header,"InvoiceDetails":inv_detail}, status=status.HTTP_200_OK)
                    elif total_bayar > total_tagihan:                
                        return Response({"pesan":"Nominal pembayaran melebihi tagihan"}, status=status.HTTP_200_OK)
                    elif total_bayar == total_tagihan:                    
                        invoice_detail.objects.create(date=now,noted=i['noted'],type_payment=i['type_payment'],
                        pay_amount=i['pay_amount'],pay_method=i['pay_method'],invoice_header_id_id=inv_header)
                        invoice_header.objects.filter(invoice_header_id=inv_header).update(status="LUNAS")
                        return Response({"pesan":"Tagihan Terbayar","Status Tagihan":"LUNAS","invoice_header_id":inv_header,"InvoiceDetails":inv_detail}, status=status.HTTP_200_OK)
                    else:                    
                        return Response({"pesan":"Terjadi kesalahan"}, status=status.HTTP_200_OK)
                else:
                    t_terbayar = invoice_detail.objects.filter(invoice_header_id_id=pk).values('invoice_header_id_id').annotate(t_terbayar=Sum('pay_amount'))[0]['t_terbayar']
                    total_bayar  = int(t_terbayar + int(i['pay_amount']))
                    if total_bayar < total_tagihan:                    
                        invoice_detail.objects.create(date=now,noted=i['noted'],type_payment=i['type_payment'],
                        pay_amount=i['pay_amount'],pay_method=i['pay_method'],invoice_header_id_id=inv_header)
                        return Response({"pesan":"Tagihan Terbayar","invoice_header_id":inv_header,"InvoiceDetails":inv_detail}, status=status.HTTP_200_OK)
                    elif total_bayar > total_tagihan:                
                        return Response({"pesan":"Nominal pembayaran melebihi tagihan"}, status=status.HTTP_200_OK)
                    elif total_bayar == total_tagihan:                    
                        invoice_detail.objects.create(date=now,noted=i['noted'],type_payment=i['type_payment'],
                        pay_amount=i['pay_amount'],pay_method=i['pay_method'],invoice_header_id_id=inv_header)
                        invoice_header.objects.filter(invoice_header_id=inv_header).update(status="LUNAS")
                        return Response({"pesan":"Tagihan Terbayar","Status Tagihan":"LUNAS","invoice_header_id":inv_header,"InvoiceDetails":inv_detail}, status=status.HTTP_200_OK)
                    else:                    
                        return Response({"pesan":"Terjadi kesalahan"}, status=status.HTTP_200_OK)
        else:
            return HttpResponse('t_terbayar')