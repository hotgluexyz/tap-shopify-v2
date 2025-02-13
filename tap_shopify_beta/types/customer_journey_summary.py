from singer_sdk import typing as th

from tap_shopify_beta.types.count import CountType
from tap_shopify_beta.types.customer_visit import CustomerVisitType

class CustomerJourneySummaryType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("customerOrderIndex", th.IntegerType),
            th.Property("daysToConversion", th.IntegerType),
            th.Property("firstVisit", CustomerVisitType()),
            th.Property("lastVisit", CustomerVisitType()),
            th.Property("momentsCount", CountType()),
            th.Property("ready", th.BooleanType),
        )
