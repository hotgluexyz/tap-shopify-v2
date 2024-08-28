from singer_sdk import typing as th

class CurrencySettingsType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("currencyCode", th.StringType),
            th.Property("currencyName", th.StringType),
            th.Property("enabled", th.BooleanType),
            th.Property("rateUpdatedAt", th.DateTimeType)
        )