from __future__ import unicode_literals

from django.db.models.signals import post_save
from django.dispatch import receiver

from cube.models import EndUserEvent
from cube.rules import (
    FirstBusinessRule,
    SecondBusinessRule,
    ThirdBusinessRule)


@receiver(post_save, sender=EndUserEvent)
def execute_product_business_rules(sender, instance, **kwargs):
    FirstBusinessRule.run_all(instance)
    SecondBusinessRule.run_all(instance)
    ThirdBusinessRule.run_all(instance)
