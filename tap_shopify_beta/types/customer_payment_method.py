from singer_sdk import typing as th

from tap_shopify_beta.types.customer import CustomerType

class CustomerPaymentMethodType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("customer", CustomerType()),
            th.Property("id", th.StringType),
            th.Property("instrument", th.StringType),
            th.Property("revokedAt", th.DateTimeType),
            th.Property("revokedReason", th.StringType),
        )