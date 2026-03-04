from singer_sdk import typing as th

from tap_shopify_beta.types.company import CompanyType

class CompanyContactType(th.ObjectType):
    def __init__(self):
        super().__init__(
            # th.Property("addresses", th.ArrayType(MailingAddressType())),
            # th.Property("amountSpent", MoneyV2Type()),
            # th.Property("canDelete", th.BooleanType),
            th.Property("company", CompanyType()),
            th.Property("id", th.StringType),
            th.Property("isMainContact", th.BooleanType),
            th.Property("lifetimeDuration", th.StringType),
            th.Property("locale", th.StringType),
            th.Property("title", th.StringType),
            th.Property("updatedAt", th.DateTimeType),
        )
