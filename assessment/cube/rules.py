from __future__ import unicode_literals

import datetime
import logging

from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_NUMERIC
from business_rules.variables import BaseVariables, numeric_rule_variable, \
    string_rule_variable, boolean_rule_variable
from django.utils import timezone
from django_business_rules.business_rule import BusinessRule
from redis import Redis
from rq_scheduler import Scheduler

from cube.models import EndUser, EndUserEvent
from assessment.constants import CUBE_SERVER

logger = logging.getLogger(CUBE_SERVER)


class FirstRuleVariables(BaseVariables):

    def __init__(self, end_user_event):
        self.end_user_event = end_user_event

    @numeric_rule_variable(label="User's bills paid since beginning of time.")
    def bills_paid(self):
        return self.end_user_event.user.bills_paid


class FirstRuleActions(BaseActions):

    def __init__(self, end_user_event):
        self.end_user_event = end_user_event

    @rule_action(label='Trigger push notification')
    def trigger_push_notification(self):
        logger.info("LOGGING LOGGING")


class FirstBusinessRule(BusinessRule):
    name = '1st business rule'
    variables = FirstRuleVariables
    actions = FirstRuleActions


class SecondRuleVariables(BaseVariables):

    def __init__(self, end_user_event):
        self.end_user_event = end_user_event

    @boolean_rule_variable(label='Bill has been paid.')
    def bill_paid(self):
        event = self.end_user_event
        if event.noun == "bill" and event.verb == "pay":
            return True
        else:
            return False
    
    @numeric_rule_variable(label='Bill pay events in past 5 minutes.')
    def bills_paid_in_past_five_minutes(self):
        event = self.end_user_event

        from datetime import timedelta

        events = EndUserEvent.objects.filter(
            timestamp__gte=event.timestamp-timedelta(minutes=5),
            timestamp__lte=event.timestamp,
            noun="bill",
            verb="pay"
        )
        return len(events)

    @numeric_rule_variable(label='Value of the bills paid in past five minutes.')
    def value_of_bills_paid(self):
        event = self.end_user_event

        from datetime import timedelta
        from django.db.models import Sum
        from django.db.models.expressions import RawSQL

        events = EndUserEvent.objects.filter(
            timestamp__gte=event.timestamp-timedelta(minutes=5),
            timestamp__lte=event.timestamp,
            noun="bill",
            verb="pay"
        ).annotate(
            val=RawSQL("((properties->>%s)::numeric)", ("value",))
        ).aggregate(sum=Sum('val'))
        
        return int(events["sum"])


class SecondRuleActions(BaseActions):

    def __init__(self, end_user_event):
        self.end_user_event = end_user_event


    @rule_action(label='Alert user')
    def alert_user(self):
        user_id = self.end_user_event.user
        logger.info("Mock alert message to user with user id - {}".format(user_id))


class SecondBusinessRule(BusinessRule):

    name = '2nd business rule'
    variables = SecondRuleVariables
    actions = SecondRuleActions


class ThirdRuleVariables(BaseVariables):
    
    def __init__(self, end_user_event):
        self.end_user_event = end_user_event
    
    @boolean_rule_variable(label='Bill has been paid.')
    def bill_paid(self):
        event = self.end_user_event
        if event.noun == "bill" and event.verb == "pay":
            return True
        else:
            return False

scheduler = Scheduler(connection=Redis()) # Get a scheduler for the "default" queue

class ThirdRuleActions(BaseActions):

    def __init__(self, end_user_event):
        self.end_user_event = end_user_event


    @rule_action(label='Alert cube operator if feedback has not been given within 15 minutes of bill payment.')
    def alert_cube_operator_if_no_feedback_15_minutes(self):
        bill_event_id = self.end_user_event.id
        event = self.end_user_event

        if not EndUserEvent.objects.filter(noun="fdbk", verb="post", properties__bill_event_id=bill_event_id):
            from datetime import timedelta
            scheduler.enqueue_at(event.timestamp + timedelta(minutes=15), 
                lambda: logger.info("Mock alert message to cube operator with phone number 91XXXXXXXXXX."))


class ThirdBusinessRule(BusinessRule):

    name = '3rd business rule'
    variables = ThirdRuleVariables
    actions = ThirdRuleActions