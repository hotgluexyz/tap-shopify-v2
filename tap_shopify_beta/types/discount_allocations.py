from singer_sdk import typing as th

from tap_shopify_beta.types.money_v2 import MoneyV2Type
from tap_shopify_beta.types.pricing_value import PricingValueType


class DiscountAllocationsType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("allocatedAmount", MoneyV2Type()),
            th.Property("discountApplication", th.ObjectType(
                th.Property("allocationMethod", th.StringType),
                th.Property("targetSelection", th.StringType),
                th.Property("targetType", th.StringType),
                th.Property("value", PricingValueType())
            ))
        )
