from django.urls import path
from django.contrib.auth import views
from .views import (
    index,
    CustomersListView,
    CustomerRecordsListView,
    CustomerRecordNewView,
    RecordDeleteView,
    CustomerRecordUpdateView,
    ProductsListView,
    ProductRecordsListView,
    ProductRecordNewView,
    ProductRecordUpdateView,
    CustomerCreateView,
    CustomerUpdateView,
    ProductCreateView,
    ProductUpdateView,
    ProductDetailsView,
    AuditoriesListView,
    AuditoryProductsListView,
    VedomostProductsListView,
    customer_create_pdf,
    vedomost_create_pdf,
)

app_name = "main"
urlpatterns = [
    path("", index, name="index"),
    path("login/", views.LoginView.as_view(template_name="main/login.html", redirect_authenticated_user=True), name="login"),
    path("logout/",views.logout_then_login, name="logout"),
    path("customers/", CustomersListView.as_view(), name="customers_list"),
    path("customers/add/", CustomerCreateView.as_view(), name="customer_add"),
    path("customers/<int:pk>/update/", CustomerUpdateView.as_view(), name="customer_update"),
    path("customers/<int:pk>/records/", CustomerRecordsListView.as_view(), name="customer_records_list"),
    path("customers/<int:pk>/records/new/", CustomerRecordNewView.as_view(), name="customer_record_add"),
    # path("customers/<int:pk_customer>/records/<int:pk>/confirm-delete/", RecordDeleteView.as_view(), name="record_delete"),
    path("customers/<int:pk_customer>/records/<int:pk>/update/", CustomerRecordUpdateView.as_view(), name="customer_record_update"),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/add/", ProductCreateView.as_view(), name="product_add"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/details/", ProductDetailsView.as_view(), name="product_details"),
    path("products/<int:pk>/records/", ProductRecordsListView.as_view(), name="product_records_list"),
    path("products/<int:pk>/records/new/", ProductRecordNewView.as_view(), name="product_record_add"),
    path("products/<int:pk_product>/records/<int:pk>/update/", ProductRecordUpdateView.as_view(),
         name="product_record_update"),
    path("auditories/", AuditoriesListView.as_view(), name="auditories_list"),
    path("auditories/products/", AuditoryProductsListView.as_view(), name="auditory_products_list"),
    path("customers/<int:pk>/records/download/", customer_create_pdf, name="customer_download"),
    path("vedomost/", VedomostProductsListView.as_view(), name="vedomost_products_list"),
    path("vedomost/download/", vedomost_create_pdf, name="vedomost_download"),
]
