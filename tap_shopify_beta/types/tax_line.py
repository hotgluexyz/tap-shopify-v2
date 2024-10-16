from singer_sdk import typing as th

from tap_shopify_beta.types.money_bag import MoneyBagType


class TaxLineType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("channelLiable", th.BooleanType),
            th.Property("priceSet", MoneyBagType()),
            th.Property("rate", th.NumberType),
            th.Property("ratePercentage", th.NumberType),
            th.Property("title", th.StringType),
        )
