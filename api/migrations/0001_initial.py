# Generated by Django 2.2.4 on 2020-02-16 14:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='groupPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(blank=True, max_length=100, null=True)),
                ('kategori', models.CharField(blank=True, max_length=100, null=True)),
                ('jenis_akses', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='master_customer',
            fields=[
                ('customer_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('customer_type', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=300, unique=True)),
                ('address', models.CharField(max_length=500)),
                ('pos_code', models.CharField(blank=True, max_length=100)),
                ('phone_code', models.CharField(blank=True, max_length=50)),
                ('phone', models.CharField(blank=True, max_length=50)),
                ('fax_code', models.CharField(blank=True, max_length=50)),
                ('fax', models.CharField(blank=True, max_length=50)),
                ('mobile_phone', models.CharField(blank=True, max_length=100)),
                ('pic_name', models.CharField(blank=True, max_length=100)),
                ('pic_number', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'db_table': 'MasterCustomer',
            },
        ),
        migrations.CreateModel(
            name='master_employee',
            fields=[
                ('employee_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('address', models.CharField(max_length=300)),
                ('id_type', models.CharField(max_length=100)),
                ('id_number', models.CharField(max_length=100)),
                ('employee_status', models.CharField(max_length=100)),
                ('dob', models.DateField()),
                ('phone_number', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'MasterEmployee',
            },
        ),
        migrations.CreateModel(
            name='master_group_item',
            fields=[
                ('group_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'MasterGroupItem',
            },
        ),
        migrations.CreateModel(
            name='master_item',
            fields=[
                ('master_item_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(blank=True, max_length=100)),
                ('counter', models.IntegerField(blank=True, null=True)),
                ('barcode', models.CharField(blank=True, max_length=100)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('alias_name', models.CharField(blank=True, max_length=200)),
                ('price1', models.CharField(max_length=200)),
                ('price2', models.CharField(blank=True, max_length=200)),
                ('price3', models.CharField(blank=True, max_length=200)),
                ('serial_number', models.BooleanField(default=True)),
                ('master_group_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='MasterGroup', to='api.master_group_item')),
            ],
            options={
                'db_table': 'MasterItem',
            },
        ),
        migrations.CreateModel(
            name='master_location',
            fields=[
                ('location_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=150)),
                ('code', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'db_table': 'MasterLokasi',
            },
        ),
        migrations.CreateModel(
            name='master_merk',
            fields=[
                ('merk_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'MasterMerk',
            },
        ),
        migrations.CreateModel(
            name='master_uom',
            fields=[
                ('uom_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'MasterUOM',
            },
        ),
        migrations.CreateModel(
            name='master_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_level', models.CharField(max_length=10)),
                ('user_type', models.CharField(max_length=10)),
                ('employee_id', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.master_employee')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'MasterUser',
            },
        ),
        migrations.CreateModel(
            name='master_vendor',
            fields=[
                ('vendor_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('address', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'MasterVendor',
            },
        ),
        migrations.CreateModel(
            name='receiving_detail',
            fields=[
                ('receiving_detail_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('qty', models.IntegerField()),
                ('note', models.CharField(blank=True, max_length=200)),
                ('master_item_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='RDItem', to='api.master_item')),
            ],
            options={
                'db_table': 'ReceivingDetail',
            },
        ),
        migrations.CreateModel(
            name='receiving_detail_sn',
            fields=[
                ('receiving_detail_sn_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('first_serial_number', models.CharField(max_length=100)),
                ('new_serial_number', models.CharField(blank=True, max_length=100)),
                ('receiving_detail_id', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='RDISN', to='api.receiving_detail')),
            ],
            options={
                'db_table': 'ReceivingDetailSN',
            },
        ),
        migrations.CreateModel(
            name='receiving_header',
            fields=[
                ('receiving_header_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(blank=True)),
                ('number', models.CharField(blank=True, max_length=100)),
                ('number_preix', models.CharField(blank=True, max_length=100)),
                ('counter', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=100)),
                ('approval1_date', models.DateField(blank=True, null=True)),
                ('approval1', models.BigIntegerField(blank=True, null=True)),
                ('note', models.CharField(blank=True, max_length=300)),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.master_location')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.master_user')),
                ('vendor_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.master_vendor')),
            ],
            options={
                'db_table': 'ReceivingHeader',
            },
        ),
        migrations.CreateModel(
            name='rental_detail',
            fields=[
                ('rental_detail_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('price', models.CharField(max_length=200)),
                ('qty', models.IntegerField()),
                ('discount_type', models.CharField(blank=True, max_length=100)),
                ('discount_method', models.CharField(blank=True, max_length=200)),
                ('discount', models.CharField(blank=True, max_length=200)),
                ('total', models.CharField(blank=True, max_length=200)),
                ('master_item_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='RentalDetailItems', to='api.master_item')),
            ],
            options={
                'db_table': 'RentalDetail',
            },
        ),
        migrations.CreateModel(
            name='rental_header',
            fields=[
                ('rental_header_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('number', models.CharField(blank=True, max_length=100)),
                ('number_prefix', models.CharField(blank=True, max_length=100)),
                ('counter', models.IntegerField(blank=True)),
                ('discount_type', models.IntegerField(blank=True, null=True)),
                ('discount', models.CharField(blank=True, max_length=100)),
                ('tax', models.CharField(blank=True, max_length=200)),
                ('delivery_cost', models.CharField(blank=True, max_length=100)),
                ('amount', models.CharField(blank=True, max_length=100)),
                ('notes', models.CharField(blank=True, max_length=500)),
                ('salesman', models.BigIntegerField(blank=True, null=True)),
                ('notes_kwitansi', models.CharField(blank=True, max_length=300)),
                ('status', models.CharField(max_length=100)),
                ('rental_start_date', models.DateField()),
                ('rental_end_date', models.DateField()),
                ('approved_by', models.BigIntegerField(blank=True, null=True)),
                ('approved_date', models.DateField(blank=True, null=True)),
                ('pay_type', models.IntegerField()),
                ('pay_method', models.IntegerField(default=None)),
                ('note_kwitansi', models.CharField(blank=True, max_length=100)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.master_customer')),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.master_location')),
            ],
            options={
                'db_table': 'RentalHeader',
            },
        ),
        migrations.CreateModel(
            name='rental_stock_card',
            fields=[
                ('stock_card_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('item_master_id', models.BigIntegerField()),
                ('location_id', models.BigIntegerField()),
                ('qty', models.IntegerField()),
                ('receiving_detail_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='RSCRD', to='api.receiving_detail')),
                ('receiving_header_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='RSCRH', to='api.receiving_header')),
                ('rental_detail_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='RSCRenD', to='api.rental_detail')),
                ('rental_header_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='RSCRenH', to='api.rental_header')),
            ],
            options={
                'db_table': 'RentalStockCard',
            },
        ),
        migrations.CreateModel(
            name='rental_stock_sn',
            fields=[
                ('stock_code_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('first_sn', models.CharField(max_length=100)),
                ('new_sn', models.CharField(blank=True, max_length=100)),
                ('status', models.CharField(blank=True, max_length=10)),
                ('receiving_detail_sn_id', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='StockSNFromRDSN', to='api.receiving_detail_sn')),
                ('stock_card_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='StockSNFromRSC', to='api.rental_stock_card')),
            ],
            options={
                'db_table': 'RentalStockSN',
            },
        ),
        migrations.CreateModel(
            name='stock_sn_history',
            fields=[
                ('stock_sn_history_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('status', models.CharField(blank=True, max_length=50)),
                ('IncomingRef_id', models.BigIntegerField(blank=True, null=True)),
                ('RentalRef_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='RentalHeader', to='api.rental_header')),
                ('stock_code_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='StockSNHistory', to='api.rental_stock_sn')),
            ],
            options={
                'db_table': 'StockSNHistory',
            },
        ),
        migrations.CreateModel(
            name='rental_order_header',
            fields=[
                ('sales_order_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('number', models.CharField(blank=True, max_length=100)),
                ('number_prefix', models.CharField(blank=True, max_length=100)),
                ('counter', models.IntegerField(blank=True)),
                ('tax', models.CharField(blank=True, max_length=200)),
                ('discount_type', models.IntegerField(blank=True, null=True)),
                ('discount', models.CharField(blank=True, max_length=100)),
                ('delivery_fee', models.CharField(blank=True, max_length=100)),
                ('amount', models.CharField(max_length=200)),
                ('notes_kwitansi', models.CharField(max_length=300)),
                ('salesman', models.BigIntegerField(blank=True, null=True)),
                ('status', models.CharField(max_length=100)),
                ('rental_start_date', models.DateField()),
                ('rental_end_date', models.DateField()),
                ('notes', models.CharField(blank=True, max_length=500)),
                ('approved_by', models.BigIntegerField(blank=True, null=True)),
                ('approved_date', models.DateField(blank=True, null=True)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.master_customer')),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.master_location')),
                ('user_id', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.master_user')),
            ],
            options={
                'db_table': 'RentalOrderHeader',
            },
        ),
        migrations.CreateModel(
            name='rental_order_detail',
            fields=[
                ('order_detail_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('price', models.CharField(max_length=200)),
                ('qty', models.IntegerField()),
                ('discount_type', models.CharField(blank=True, max_length=100)),
                ('discount_method', models.CharField(blank=True, max_length=100)),
                ('discount', models.CharField(blank=True, max_length=200)),
                ('total', models.CharField(max_length=200)),
                ('master_item_id', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.master_item')),
                ('sales_order_id', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='RODHeader', to='api.rental_order_header')),
            ],
            options={
                'db_table': 'RentalOrderDetail',
            },
        ),
        migrations.AddField(
            model_name='rental_header',
            name='sales_order_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.rental_order_header'),
        ),
        migrations.AddField(
            model_name='rental_header',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.master_user'),
        ),
        migrations.CreateModel(
            name='rental_detail_sn',
            fields=[
                ('rental_detail_sn_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('rental_detail_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='RDSN', to='api.rental_detail')),
                ('stock_code_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.rental_stock_sn')),
            ],
        ),
        migrations.AddField(
            model_name='rental_detail',
            name='order_detail_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='RentalDetailROD', to='api.rental_order_detail'),
        ),
        migrations.AddField(
            model_name='rental_detail',
            name='rental_header_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='RentalDetailHeader', to='api.rental_header'),
        ),
        migrations.AddField(
            model_name='receiving_detail',
            name='receiving_header_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='RDHeader', to='api.receiving_header'),
        ),
        migrations.AddField(
            model_name='receiving_detail',
            name='uom_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='RDUom', to='api.master_uom'),
        ),
        migrations.AddField(
            model_name='master_item',
            name='merk_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.master_merk'),
        ),
        migrations.AddField(
            model_name='master_item',
            name='uom_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.master_uom'),
        ),
        migrations.CreateModel(
            name='invoice_header',
            fields=[
                ('invoice_header_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(blank=True)),
                ('amount', models.CharField(blank=True, max_length=100)),
                ('customer', models.BigIntegerField(blank=True)),
                ('pay_method', models.IntegerField(blank=True)),
                ('status', models.CharField(blank=True, max_length=50)),
                ('rental_header_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.rental_header')),
            ],
            options={
                'db_table': 'InvoiceHeader',
            },
        ),
        migrations.CreateModel(
            name='invoice_detail',
            fields=[
                ('invoice_detail_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(blank=True)),
                ('type_payment', models.CharField(blank=True, max_length=50)),
                ('pay_amount', models.BigIntegerField(blank=True)),
                ('pay_method', models.CharField(blank=True, max_length=50)),
                ('noted', models.TextField(blank=True)),
                ('jml_period', models.IntegerField(blank=True, null=True)),
                ('period', models.CharField(blank=True, max_length=50)),
                ('harga_rental', models.CharField(blank=True, max_length=200)),
                ('invoice_header_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='InvoiceDetails', to='api.invoice_header')),
                ('master_item_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Items', to='api.master_item')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.master_user')),
            ],
            options={
                'db_table': 'InvoiceDetail',
            },
        ),
    ]