# Explanation of design via example

Let's take a look at a quick example.

## Setup

Startup up a new project like so...

    pip install django django-business-rules
    django-admin.py startproject example .
    ./manage.py startapp test_app


Now edit the `example/urls.py` module in your project (django 2.x):

```python
from django.urls import include, path, re_path

# Include the business rules URLconf
urlpatterns = [
    ...
    re_path(r'^dbr/', include('django_business_rules.urls', namespace='django_business_rules'))
]
```

Now edit the `example/urls.py` module in your project (django 1.x):

```python
from django.conf.urls import include, url

# Include the business rules URLconf
urlpatterns = [
    ...
    url(r'^dbr/', include('django_business_rules.urls', namespace='django_business_rules'))
]
```

Add the following to your `example/settings.py` module:

```python
INSTALLED_APPS = (
    ...  # Make sure to include the default installed apps here.
    'django_business_rules',
    'test_app.apps.TestAppConfig',
)
```

## Usage

Add models to your `test_app/model.py` module:

```python
from django.db import models


class Product(models.Model):
    name = models.TextField()
    related_products = models.ManyToManyField('Product', blank=True)
    current_inventory = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    @property
    def orders(self):
        return list(self.productorder_set.all())


class ProductOrder(models.Model):
    expiration_date = models.DateField()
    quantity = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
```

Add variables and actions to your `test_app/rules.py` module (more about variables and actions can be found [here][https://github.com/venmo/business-rules]):

```python
import datetime

from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_NUMERIC
from business_rules.variables import BaseVariables, numeric_rule_variable, \
    string_rule_variable, select_rule_variable
from django.utils import timezone
from django_business_rules.business_rule import BusinessRule

from test_app.models import Product, ProductOrder


class ProductVariables(BaseVariables):

    def __init__(self, product):
        self.product = product

    @numeric_rule_variable
    def current_inventory(self):
        return self.product.current_inventory

    @numeric_rule_variable(label='Days until expiration')
    def expiration_days(self):
        last_order = self.product.orders[-1]
        expiration_days = (last_order.expiration_date - datetime.date.today()).days
        return expiration_days

    @string_rule_variable()
    def current_month(self):
        return timezone.now().strftime('%B')


class ProductActions(BaseActions):

    def __init__(self, product):
        self.product = product

    @rule_action(params={'sale_percentage': FIELD_NUMERIC})
    def put_on_sale(self, sale_percentage):
        self.product.price *= (1.0 - sale_percentage)
        self.product.save()

    @rule_action(params={'number_to_order': FIELD_NUMERIC})
    def order_more(self, number_to_order):
        ProductOrder.objects.create(
            product=self.product,
            quantity=number_to_order,
            expiration_date=timezone.now() + timezone.timedelta(weeks=4)
        )


class ProductBusinessRule(BusinessRule):
    name = 'Product rules'
    variables = ProductVariables
    actions = ProductActions
```

Add triggering defined rules on django post_save signal to your `test_app/signals.py` module:

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

from test_app.models import Product
from test_app.rules import ProductBusinessRule


@receiver(post_save, sender=Product)
def execute_product_business_rules(sender, instance, **kwargs):
    ProductBusinessRule.run_all(instance)
```

Register signals in `test_app/apps.py` module:

```python
class TestAppConfig(AppConfig):
    name = 'test_app'

    def ready(self):
        import test_app.signals
```

Create and execute migrations:

    ./manage.py makemigrations
    ./manage.py migrate

Generate business rules (currently this command doesn't support updates, previously stored business rules data will be overridden):

    ./manage.py dbr

That's it, we're done!

    ./manage.py runserver

You can now open the list of business rules in your browser at `http://127.0.0.1:8000/dbr/business-rule/` and edit them.
