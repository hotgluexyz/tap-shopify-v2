from singer_sdk import typing as th


class MoneyV2Type(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("amount", th.StringType),
            th.Property("currencyCode", th.StringType)
        )
