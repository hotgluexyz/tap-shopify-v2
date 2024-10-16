from singer_sdk import typing as th

from tap_shopify_beta.types.money_v2 import MoneyV2Type


class MoneyBagType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("presentmentMoney", MoneyV2Type()),
            th.Property("shopMoney", MoneyV2Type()),
        )
