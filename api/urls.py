from rest_framework import routers
from django.conf.urls import include
from django.conf.urls import url
from .viewset import *
from .views.users import testView, MasterUser
from .views import auth, employee, items, stock, rentals, invoice

router = routers.DefaultRouter()
router.register(r'master_kategori', master_kategori)  # Master management starts here
router.register(r'master_uom', master_unit)
router.register(r'master_merk', master_merk)
router.register(r'master_location', master_location)
router.register(r'master_vendor', master_vendor)
router.register(r'master_customer', master_pelanggan)
router.register(r'master_item', master_item)
router.register(r'master_user', master_user)
router.register(r'master_employee', master_employee)
router.register(r'receiving_detail_sn', receiving_detail_sn)  # Receiving Management starts here
router.register(r'receiving_detail', receiving_detail)
router.register(r'receiving_header', receiving_header)
router.register(r'rental_order_header', rental_order_header)
router.register(r'rental_order_detail', rental_order_detail)
router.register(r'rental_header', rental_header)  # Rental management starts here
router.register(r'rental_detail', rental_detail)
router.register(r'rental_stock_card', rental_stock_card)  # Stock management starts here
router.register(r'rental_stock_sn', rental_stock_sn)
router.register(r'stock_sn_history', stock_sn_history)
router.register(r'invoice_header', invoice_header)
router.register(r'invoice_detail', invoice_detail)

urlpatterns = {
	url(r'^', include(router.urls)),
	url(r'^testView/', testView),
	url(r'^masterUser/', MasterUser.as_view()),

	# authenticate
	url(r'^signup/', auth.signup, name='signup'),
	url(r'^makeGroupPermission/', auth.createGroup, name="createGroup"),
	url(r'^getUser/', auth.getUser, name="GetUser"),
	url(r'^assignGroup/', auth.assignGroupToUser, name="AssignGroupToUser"),
	url(r'^removeGroupFromUser/', auth.removeGroupFromUser, name="RemoveGroupFromUser"),
	url(r'^editGroup/', auth.editGroup, name="EditGroup"),
	url(r'^getAllGroup/', auth.getAllGroups, name="GetAllGroups"),
	url(r'^PermissiongetAllGroup/', auth.getAllGroupsPermission, name="getAllGroupsPermission"),

	# employee
	url(r'^MasterEmployee/', employee.MasterEmployee.as_view(), name="MasterEmployee"),

	# items
	url(r'getItemByCat/(?P<b>\d+)/$', items.getItemByCategory, name='GetItemByCategory'),
    url(r'getItemByBarcode/(?P<b>\d+)/$', items.getItemByBarcode, name='GetItemByBarcode'),
    url(r'getItemSNs/(?P<i>\d+)/$', items.getItemSNs, name='GetSNsByItem'),
    url(r'getItemSNsAvailable/(?P<i>\d+)/$', items.getItemSNsAvailable, name='GetSNsByItemAvailable'),
    url(r'^getUnapprovedHeader/(\d+)/', items.getUnapprovedHeader, name="GetUnapprovedHeader"),
    url(r'^getDistinctStocks/', items.getDistinctItem, name="GetDistinctStock"),

    # stok 
    url(r'^NestedStockManagement/', stock.NestedStockManagement.as_view()),
    url(r'^NestedStockManagementDetails/(?P<pk>\d+)/$', stock.NestedStockManagementDetails.as_view()),
    url(r'^StockNestedSNhistory', stock.NestedStockSNhistory.as_view(), name="NestedStockSNhistory"),

    # Rental
    url(r'^NestedRentalRegister/', rentals.NestedRentalRegister.as_view()),
    url(r'^NestedKembaliRentalRegister/', rentals.NestedKembaliRentalRegister.as_view()),
    url(r'^NestedRentalRegisterDetails/(?P<pk>[0-9]+)/$', rentals.NestedRentalRegisterDetails.as_view()),
    url(r'^NestedRentalOrderManagement/', rentals.NestedRentalOrderManagement.as_view()),
    url(r'^NestedRentalOrderManagementDetails/(?P<pk>[0-9]+)/$', rentals.NestedRentalOrderManagementDetails.as_view()),
    url(r'^NestedRentalExtend/$', rentals.extendRental, name='rentalExtend'),
    url(r'^NestedReceivingManagement/', rentals.NestedReceivingManagement.as_view()),
    url(r'^NestedReceivingManagementDetails/(?P<pk>\d+)/$', rentals.NestedReceivingManagementDetails.as_view()),
    url(r'getRentalOrderHeaderApproved/', rentals.getAllRentalOrderApproved, name="GetAllRentalRegisterApproved"),

    # invoice
    url(r'^ByIDNestedInvoiceManagement/(?P<pk>\d+)/$', invoice.NestedInvoiceManagementByID.as_view(),
        name="NestedInvoiceManagementByID"),
    url(r'^NestedInvoiceManagement/', invoice.NestedInvoiceManagement.as_view()),
    url(r'^NestedInvoiceManagementDetails/(?P<pk>[0-9]+)/$', invoice.NestedInvoiceManagementDetails.as_view()),
}