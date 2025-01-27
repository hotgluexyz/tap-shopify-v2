from singer_sdk import typing as th


from tap_shopify_beta.types.count import CountType
from tap_shopify_beta.types.money_v2 import MoneyV2Type

class CompanyType(th.ObjectType):
    def __init__(self):
        super().__init__(
            # th.Property("contactsCount", CountType()),
            th.Property("createdAt", th.DateTimeType),
            th.Property("customerSince", th.DateTimeType),
            th.Property("defaultCursor", th.StringType),
            th.Property("defaultRole", th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("name", th.StringType),
                th.Property("note", th.StringType),
            )),
            th.Property("externalId", th.StringType),
            th.Property("hasTimelineComment", th.BooleanType),
            th.Property("id", th.StringType),
            th.Property("lifetimeDuration", th.StringType),
            # th.Property("locationsCount", CountType()),
            th.Property("externalId", th.StringType),
            th.Property("name", th.StringType),
            th.Property("note", th.StringType),
            # th.Property("ordersCount", CountType()),
            th.Property("totalSpent", MoneyV2Type()),
            th.Property("updatedAt", th.DateTimeType),
        )