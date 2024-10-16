from singer_sdk import typing as th
from tap_shopify_beta.types.money_v2 import MoneyV2Type
from tap_shopify_beta.types.pricing_percentage_value import PricingPercentageValueType

class PricingValueType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("... on MoneyV2", MoneyV2Type()),
            th.Property("... on PricingPercentageValue", PricingPercentageValueType()),
        )
