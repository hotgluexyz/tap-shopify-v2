from singer_sdk import typing as th

from tap_shopify_beta.types.market import MarketType

class TranslationType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("key", th.StringType),
            th.Property("locale", th.StringType),
            th.Property("market", MarketType()),
            th.Property("outdated", th.BooleanType),
            th.Property("updatedAt", th.DateTimeType),
            th.Property("value", th.StringType),
        )
                        