from django.db import models

# Create your models here.

class ProductType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"

class Product(models.Model):
    name = models.CharField("Наименование", max_length=100)
    description = models.TextField("Описание", blank=True)
    identity_number = models.CharField("Инвентарный номер", max_length=10)
    price = models.DecimalField("Стоимость", default=0, max_digits=10, decimal_places=2)
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    producttype = models.ForeignKey(ProductType, on_delete=models.PROTECT)
    start_job = models.DateField('Поступление', null=True, blank=True)
    stop_job = models.DateField('Списание', null=True, blank=True)

    def __str__(self):
        return f"{self.identity_number}--{self.name}"

    def description_short(self):
        if len(self.description) < 28:
            return self.description
        return self.description[:28] + "..."

    def name_short(self):
        if len(self.name) < 30:
            return self.name
        return self.name[:30] + "..."

    class Meta:
        ordering = ["identity_number"]
        unique_together = ["identity_number", "name"]

class Customer(models.Model):
    surname = models.CharField('Фамилия', max_length=15)
    name = models.CharField('Имя', max_length=15)
    middlename = models.CharField('Отчество', max_length=15)
    position = models.CharField('Должность', max_length=30, blank=True)
    house = models.CharField('Корпус', max_length=3)
    auditory = models.CharField('Кабинет', max_length=4)
    telephone = models.CharField('Телефон', max_length=4)
    start_job = models.DateField('Поступил на работу', null=True, blank=True, default=None)
    stop_job = models.DateField('Уволился с работы', null=True, blank=True, default=None)
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def fio(self):
        return f"{self.surname} {self.name} {self.middlename}"

    def house_auditory(self):
        return f"{self.house}-{self.auditory}"

    def __str__(self):
        return self.fio()

    class Meta:
        ordering = ["surname", "name"]
        unique_together = ["surname", "name", "middlename"]

class Record(models.Model):
    set_date = models.DateField("Дата выдачи", null=True)
    unset_date = models.DateField("Дата возврата", null=True, blank=True)
    description = models.TextField("Примечание", null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    class Meta:
        ordering = ["set_date"]
