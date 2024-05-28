
from django.http import HttpRequest, HttpResponse, FileResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.views import View
from django.db.models import Prefetch, Q

from main.forms import CustomerRecordNewForm, RecordUpdateForm, ProductRecordNewForm
from main.models import Customer, Record, Product

from .reportlab_mixins import PDFCreator


# Create your views here.
def index(request: HttpRequest):
    context = {

    }
    return render(request, 'main/index.html', context=context)

class CustomersListView(ListView):
    template_name = "main/customers-list.html"
    # paginate_by = 50
    context_object_name = "customers"
    def get_queryset(self):
        name = self.request.GET['name'] if "name" in self.request.GET else ""
        queryset = (Customer.objects
        .filter(
            Q(surname__icontains=name) |
            Q(name__icontains=name) |
            Q(middlename__icontains=name) |
            Q(telephone__icontains=name) |
            Q(auditory__icontains=name)
        ).prefetch_related(
            Prefetch('record_set', queryset=Record.objects.filter(unset_date=None).select_related("product"))
        ))
        return queryset

class CustomerRecordsListView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        customer = get_object_or_404(Customer, pk=pk)
        records = customer.record_set.all()
        context = {
            "customer": customer,
            "records": records,
        }
        return render(request, 'main/customer-records.html', context=context)

class CustomerRecordNewView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        customer = get_object_or_404(Customer, pk=pk)
        form = CustomerRecordNewForm()
        context = {
            "form": form,
            "customer": customer,
        }
        return render(request, 'main/customer-record-add.html', context=context)

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        customer = get_object_or_404(Customer, pk=pk)
        form = CustomerRecordNewForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.customer = customer
            record.save()
            url = reverse("main:customer_records_list", kwargs={"pk": customer.pk})
            return redirect(url)

        return redirect(request.path)

class CustomerRecordUpdateView(UpdateView):
    model = Record
    template_name_suffix = '_update_form'
    form_class = RecordUpdateForm

    def get_success_url(self):
        return reverse(
            "main:customer_records_list",
            kwargs={"pk": self.object.customer.pk},
        )

class CustomerCreateView(CreateView):
    model = Customer
    fields = (
        "surname",
        "name",
        "middlename",
        "position",
        "house",
        "auditory",
        "telephone",
        "start_job",
    )
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('main:customers_list')

class CustomerUpdateView(UpdateView):
    model = Customer
    fields = (
        "surname",
        "name",
        "middlename",
        "position",
        "house",
        "auditory",
        "telephone",
        "start_job",
        "stop_job",
    )
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('main:customers_list')

    def form_valid(self, form):
        if form.instance.stop_job:
            form.instance.archived = True
        else:
            form.instance.archived = False

        return super().form_valid(form)

class ProductsListView(ListView):
    template_name = "main/products-list.html"
    # paginate_by = 50
    context_object_name = "products"

    def get_queryset(self):
        name = self.request.GET['name'] if "name" in self.request.GET else ""
        queryset = Product.objects.filter(Q(identity_number__icontains=name) | Q(name__icontains=name)).prefetch_related(
            Prefetch('record_set', queryset=Record.objects.filter(unset_date=None).select_related("customer"))
        )
        return queryset

class ProductRecordsListView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        product = get_object_or_404(Product, pk=pk)
        records = product.record_set.all()
        context = {
            "product": product,
            "records": records,
        }
        return render(request, 'main/product-records.html', context=context)

class ProductRecordNewView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        product = get_object_or_404(Product, pk=pk)
        form = ProductRecordNewForm()
        context = {
            "form": form,
            "product": product,
        }
        return render(request, 'main/product-record-add.html', context=context)

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        product = get_object_or_404(Product, pk=pk)
        form = ProductRecordNewForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.product = product
            record.save()
            url = reverse("main:product_records_list", kwargs={"pk": product.pk})
            return redirect(url)

        return redirect(request.path)

class ProductRecordUpdateView(UpdateView):
    model = Record
    template_name_suffix = '_update_form'
    form_class = RecordUpdateForm

    def get_success_url(self):
        return reverse(
            "main:product_records_list",
            kwargs={"pk": self.object.product.pk},
        )

class RecordDeleteView(DeleteView):
    model = Record
    # success_url = reverse_lazy("main:customers_list")
    def get_success_url(self):
        return reverse(
            "main:customer_records_list",
            kwargs={"pk": self.object.customer.pk},
        )

class ProductCreateView(CreateView):
    model = Product
    fields = (
        "name",
        "description",
        "identity_number",
        "price",
        "producttype",
    )
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('main:products_list')

class ProductUpdateView(UpdateView):
    model = Product
    fields = (
        "name",
        "description",
        "identity_number",
        "price",
        "producttype",
    )
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('main:products_list')

class ProductDetailsView(DetailView):
    template_name = "main/product-details.html"
    model = Product
    context_object_name = "product"

class AuditoriesListView(ListView):
    template_name = "main/auditories-list.html"
    context_object_name = "customers"
    queryset = Customer.objects.all().prefetch_related(
        Prefetch('record_set', queryset=Record.objects.filter(unset_date=None))
    )
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customers = context['object_list']
        auditories = {}
        for customer in customers:
            if customer.house_auditory() in auditories:
                auditories[customer.house_auditory()] += customer.record_set.count()
            elif customer.record_set.count() > 0:
                auditories[customer.house_auditory()] = customer.record_set.count()

        auditories = dict(sorted(auditories.items()))
        context['auditories'] = auditories
        return context

class AuditoryProductsListView(ListView):
    template_name = "main/auditory-products-list.html"
    context_object_name = "customers"

    def get_queryset(self):
        param = self.request.GET['house_auditory'] if "house_auditory" in self.request.GET else ""
        param = param.split("-")
        house = auditory = "none"
        if len(param) == 2:
            house = param[0]
            auditory = param[1]
        queryset = Customer.objects.filter(house__exact=house, auditory__exact=auditory).prefetch_related(
            Prefetch('record_set', queryset=Record.objects.filter(Q(unset_date=None)).select_related("product"))
        )
        return queryset

def customer_create_pdf(request: HttpRequest, pk: int):
    if not request.user.is_authenticated:
        return redirect(reverse('main:login'))

    pdf = PDFCreator()
    return pdf.create_for_customer(request, pk)
