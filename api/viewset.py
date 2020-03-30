from rest_framework import viewsets, permissions
from .serializers import *
from .models import *


class master_kategori(viewsets.ModelViewSet):
    queryset = master_group_item.objects.all()
    serializer_class = CategorySerializer


class master_unit(viewsets.ModelViewSet):
    queryset = master_uom.objects.all()
    serializer_class = UOMSerializer


class master_user(viewsets.ModelViewSet):
    queryset = master_user.objects.all()
    serializer_class = UserSerializer


class master_merk(viewsets.ModelViewSet):
    queryset = master_merk.objects.all()
    serializer_class = MerkSerializer


class master_location(viewsets.ModelViewSet):
    queryset = master_location.objects.all()
    serializer_class = LocationSerializer


class master_vendor(viewsets.ModelViewSet):
    queryset = master_vendor.objects.all()
    serializer_class = VendorSerializer


class master_pelanggan(viewsets.ModelViewSet):
    queryset = master_customer.objects.all()
    serializer_class = CustomerSerializer


class master_employee(viewsets.ModelViewSet):
    queryset = master_employee.objects.all()
    serializer_class = EmployeeSerializer


class master_item(viewsets.ModelViewSet):
    queryset = master_item.objects.all()

    def get_serializer_class(self):
        if self.action == 'list' or self.action =='retrieve':
            return ItemReadSerializer
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return ItemWriteSerializer


class receiving_detail(viewsets.ModelViewSet):
    queryset = receiving_detail.objects.all()
    serializer_class = ReceivingDetailSerializer


class receiving_header(viewsets.ModelViewSet):
    queryset = receiving_header.objects.all()
    serializer_class = ReceivingHeaderSerializer


class receiving_detail_sn(viewsets.ModelViewSet):
    queryset = receiving_detail_sn.objects.all()
    serializer_class = ReceivingDetailSNSerializer


class rental_order_header(viewsets.ModelViewSet):
    queryset = rental_order_header.objects.all()
    serializer_class = RentalOrderHeaderSerializer


class rental_order_detail(viewsets.ModelViewSet):
    queryset = rental_order_detail.objects.all()
    serializer_class = RentalOrderDetailSerializer


class rental_header(viewsets.ModelViewSet):
    queryset = rental_header.objects.all()
    serializer_class = RentalHeaderSerializer


class rental_detail(viewsets.ModelViewSet):
    queryset = rental_detail.objects.all()
    serializer_class = RentalDetailSerializer


class rental_stock_card(viewsets.ModelViewSet):
    queryset = rental_stock_card.objects.all()
    serializer_class = RentalStockCardSerializer


class rental_stock_sn(viewsets.ModelViewSet):
    queryset = rental_stock_sn.objects.all()
    serializer_class = RentalStockSNSerializer


class stock_sn_history(viewsets.ModelViewSet):
    queryset = stock_sn_history.objects.all()
    serializer_class = StockSNHistorySerializer


class invoice_header(viewsets.ModelViewSet):
    queryset = invoice_header.objects.all()
    serializer_class = InvoiceHeaderSerializer

class invoice_detail(viewsets.ModelViewSet):
    queryset = invoice_detail.objects.all()
    serializer_class = InvoiceDetailSerializer

# class InvoiceHeaderViewSet(viewsets.ModelViewSet):
#     queryset = invoice_header.objects.all()
#     serializer_class = NestedInvoiceReadSerializerNew
#     def get_queryset(self):
#         return invoice_header.objects.values('date','amount','invoice_header_id','rental_header_id','status').annotate(
#             t_terbayar=Sum('InvoiceDetails__pay_amount')
#             ).order_by('invoice_header_id')