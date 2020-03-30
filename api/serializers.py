from rest_framework import serializers
from .models import *
from .models.rental_register_detail import rental_detail_sn
from .models.master_employee import groupPermission
from drf_writable_nested import WritableNestedModelSerializer
from django.contrib.auth.models import User, Group, Permission


# Master Management
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = master_group_item
        fields = '__all__'


class UOMSerializer(serializers.ModelSerializer):
    class Meta:
        model = master_uom
        fields = '__all__'


class MerkSerializer(serializers.ModelSerializer):
    class Meta:
        model = master_merk
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = master_location
        fields = '__all__'


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = master_vendor
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = master_customer
        fields = '__all__'


class ItemReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = master_item
        # depth = 2
        fields = '__all__'


class ItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = master_item
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = master_user
        depth = 2
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = master_employee
        fields = '__all__'


# Receiving Management

class ReceivingDetailSNSerializer(serializers.ModelSerializer):
    class Meta:
        model = receiving_detail_sn
        fields = '__all__'


class ReceivingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = receiving_detail
        fields = '__all__'


class ReceivingHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = receiving_header
        fields = '__all__'

class GroupPermission(serializers.ModelSerializer):
    class Meta:
        model = groupPermission
        fields = '__all__'

class NestedReceivingDetailReadSerializer(WritableNestedModelSerializer):
    RDISN = ReceivingDetailSNSerializer(many=True)

    class Meta:
        model = receiving_detail
        depth = 2
        fields = ['receiving_detail_id', 'qty', 'note', 'receiving_header_id', 'master_item_id', 'uom_id', 'RDISN']

class NestedMasterItemReadSerializer(WritableNestedModelSerializer):    
    class Meta:
        model = master_item
        depth = 2
        fields = ['master_item_id', 'code', 'counter', 'barcode', 'name', 'alias_name', 'price1',
        'price2','price3','master_group_id','uom_id','merk_id', 'serial_number']            


class NestedReceivingDetailWriteSerializer(WritableNestedModelSerializer):
    RDISN = ReceivingDetailSNSerializer(many=True)

    class Meta:
        model = receiving_detail
        fields = ['receiving_detail_id', 'qty', 'note', 'receiving_header_id', 'master_item_id', 'uom_id', 'RDISN']


class NestedReceivingHeaderReadSerializer(WritableNestedModelSerializer):
    RDHeader = NestedReceivingDetailReadSerializer(many=True)

    class Meta:
        model = receiving_header
        fields = ['receiving_header_id', 'date', 'number', 'number_preix', 'counter', 'status', 'approval1_date',
                  'approval1', 'note', 'vendor_id', 'location_id', 'user_id', 'RDHeader']


class NestedReceivingHeaderWriteSerializer(WritableNestedModelSerializer):
    RDHeader = NestedReceivingDetailWriteSerializer(many=True)

    class Meta:
        model = receiving_header
        fields = ['receiving_header_id', 'date', 'number', 'number_preix', 'counter', 'status', 'approval1_date',
                  'approval1', 'note', 'vendor_id', 'location_id', 'user_id', 'RDHeader']


# Rental Order Management

class RentalOrderHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = rental_order_header
        fields = '__all__'


class RentalOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = rental_order_detail
        fields = '__all__'


class RentalOrderDetailReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = rental_order_detail
        depth = 2
        fields = '__all__'


class NestedRentalOrderHeaderReadSerializer(WritableNestedModelSerializer):
    RODHeader = RentalOrderDetailReadSerializer(many=True)

    class Meta:
        model = rental_order_header
        depth = 2
        fields = ['sales_order_id', 'date', 'number', 'number_prefix', 'counter', 'tax', 'discount_type', 'discount',
                  'delivery_fee', 'amount', 'notes_kwitansi', 'salesman', 'status', 'rental_start_date',
                  'rental_end_date', 'notes', 'location_id', 'customer_id', 'approved_by', 'approved_date', 'user_id',
                  'RODHeader']


class NestedRentalOrderHeaderWriteSerializer(WritableNestedModelSerializer):
    RODHeader = RentalOrderDetailSerializer(many=True)

    class Meta:
        model = rental_order_header
        fields = ['sales_order_id', 'date', 'number', 'number_prefix', 'counter', 'tax', 'discount_type', 'discount',
                  'delivery_fee', 'amount', 'notes_kwitansi', 'salesman', 'status', 'rental_start_date',
                  'rental_end_date', 'notes', 'location_id', 'customer_id', 'approved_by', 'approved_date', 'user_id',
                  'RODHeader']


# Stock Management

class RentalStockCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = rental_stock_card
        fields = '__all__'


class RentalStockSNSerializer(serializers.ModelSerializer):
    class Meta:
        model = rental_stock_sn
        fields = '__all__'


class StockSNHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = stock_sn_history
        fields = '__all__'

class NestedStockSNHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = stock_sn_history
        depth = 2
        fields = ['stock_sn_history_id','date','status','IncomingRef_id','RentalRef_id','stock_code_id']

class NestedStockSNSerializer(WritableNestedModelSerializer):
    StockSNHistory = StockSNHistorySerializer(many=True)

    class Meta:
        model = rental_stock_sn
        fields = ['stock_code_id', 'first_sn', 'new_sn', 'receiving_detail_sn_id', 'stock_card_id', 'StockSNHistory']


class NestedStockCardSerializer(WritableNestedModelSerializer):
    StockSNFromRSC = NestedStockSNSerializer(many=True)

    class Meta:
        model = rental_stock_card
        depth = 4
        fields = ['stock_card_id', 'item_master_id', 'location_id', 'qty', 'rental_header_id', 'rental_detail_id',
                  'receiving_header_id', 'receiving_detail_id', 'StockSNFromRSC']


# Rental Management (Invoicing)

class InvoiceHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = invoice_header
        fields = '__all__'


class InvoiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = invoice_detail
        fields = '__all__'

class NestedInvoiceSerializer(WritableNestedModelSerializer):
    InvoiceDetails = InvoiceDetailSerializer(many=True,read_only=True)

    class Meta:
        model = invoice_header
        fields = ['invoice_header_id', 'date', 'amount', 'customer', 'pay_method', 'rental_header_id', 'InvoiceDetails']

class NestedInvoiceDetailReadSerializer(WritableNestedModelSerializer):

    class Meta:
        model = invoice_detail
        depth = 2
        fields = ['invoice_detail_id', 'date', 'type_payment', 'pay_amount', 'pay_method', 'noted',
        'user_id','jml_period','period','harga_rental','master_item_id']

class NestedInvoiceReadSerializer(WritableNestedModelSerializer):
    InvoiceDetails = NestedInvoiceDetailReadSerializer(many=True)

    class Meta:
        model = invoice_header
        fields = ['invoice_header_id','InvoiceDetails']

#proses perbaikan
class NestedInvoiceReadSerializerNew(WritableNestedModelSerializer):
    t_terbayar = serializers.IntegerField()    

    class Meta:
        model = invoice_header
        depth = 5
        fields = ['date','amount','invoice_header_id','status','t_terbayar','rental_header_id']
#proses perbaikan

# Rental Register
# mulai dari sini

class RentalDetailWriteSnSerializer(serializers.ModelSerializer):
    StokCode = RentalStockSNSerializer(many=True)
    class Meta:
        model = rental_detail_sn
        fields = '__all__'

class RentalDetailSnSerializer(serializers.ModelSerializer):
    class Meta:
        model = rental_detail_sn
        fields = '__all__'

class RentalDetailSerializer(serializers.ModelSerializer):    
    class Meta:
        model = rental_detail
        fields = '__all__'

class RentalHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = rental_header
        fields = '__all__'
#tambah
class NestedRentalDetailSNReadSerializer(WritableNestedModelSerializer):

    class Meta:
        model = rental_detail_sn
        depth = 2
        fields = ['rental_detail_sn_id', 'rental_detail_id', 'stock_code_id']

class NestedRentalDetailSNWriteSerializer(WritableNestedModelSerializer):
    class Meta:
        model = rental_detail_sn        
        fields = ['rental_detail_sn_id', 'rental_detail_id', 'stock_code_id']

class NestedRentalDetailReadSerializer(WritableNestedModelSerializer):
    RDSN = NestedRentalDetailSNReadSerializer(many=True)    

    class Meta:
        model = rental_detail
        depth = 2
        fields = ['rental_detail_id', 'price', 'qty', 'discount_type', 'discount_method', 'discount', 'total',
        'rental_header_id','order_detail_id','master_item_id','RDSN']


class NestedReadRentalDetail(WritableNestedModelSerializer):
    class Meta:
        model = rental_detail
        depth = 1
        fields = ['rental_detail_id','master_item_id']

# class NestedReadMasterUser(WritableNestedModelSerializer):
#     class Meta:
#         model = master_user
#         depth = 2
#         fields = ['user_level','user_type','user']

class NestedRentalDetailWriteSerializer(WritableNestedModelSerializer):
    # menambahkan ini 
    RDSN = NestedRentalDetailSNWriteSerializer(many=True)

    class Meta:
        model = rental_detail
        fields = ['rental_detail_id', 'price', 'qty', 'discount_type', 'discount_method', 'discount', 'total',
        'rental_header_id','order_detail_id','master_item_id','RDSN']


class NestedRentalHeaderReadSerializer(WritableNestedModelSerializer):
    RentalDetailHeader = NestedRentalDetailReadSerializer(many=True)

    class Meta:
        model = rental_header
        fields = ['rental_header_id', 'date', 'user_id', 'number', 'number_prefix', 'counter', 'discount_type',
                  'discount', 'tax', 'delivery_cost', 'amount', 'notes', 'salesman', 'notes_kwitansi', 'status',
                  'rental_start_date', 'rental_end_date', 'sales_order_id', 'customer_id', 'location_id',
                  'approved_by', 'approved_date', 'pay_type', 'pay_method', 'note_kwitansi', 'RentalDetailHeader']
# tambah
class NestedRentalHeaderWriteSerializer(WritableNestedModelSerializer):
    RentalDetailHeader = NestedRentalDetailWriteSerializer(many=True)    

    class Meta:
        model = rental_header
        fields = ['rental_header_id', 'date', 'user_id', 'number', 'number_prefix', 'counter', 'discount_type',
                  'discount', 'tax', 'delivery_cost', 'amount', 'notes', 'salesman', 'notes_kwitansi', 'status',
                  'rental_start_date', 'rental_end_date', 'sales_order_id', 'customer_id', 'location_id',
                  'approved_by', 'approved_date', 'pay_type', 'pay_method', 'note_kwitansi', 'RentalDetailHeader']