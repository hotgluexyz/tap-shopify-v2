from singer_sdk import typing as th

class AppSubscriptionType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("createdAt", th.DateTimeType),
            th.Property("currentPeriodEnd", th.DateTimeType),
            th.Property("id", th.StringType),
            th.Property("lineItems", th.ArrayType(th.ObjectType(
                th.Property("id", th.StringType)
            ))),
            th.Property("name", th.StringType),
            th.Property("returnUrl", th.StringType),
            th.Property("status", th.StringType),
            th.Property("test", th.BooleanType),
            th.Property("trialDays", th.IntegerType)
        )
