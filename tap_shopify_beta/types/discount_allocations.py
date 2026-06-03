from hotglue_singer_sdk import typing as th

from tap_shopify_beta.types.money_bag import MoneyBagType
from tap_shopify_beta.types.pricing_value import PricingValueType


class DiscountAllocationsType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("allocatedAmountSet", MoneyBagType()),
            th.Property("discountApplication", th.ObjectType(
                th.Property("allocationMethod", th.StringType),
                th.Property("targetSelection", th.StringType),
                th.Property("targetType", th.StringType),
                th.Property("value", PricingValueType()),
                th.Property("index", th.IntegerType())
            ))
        )
