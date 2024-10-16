from singer_sdk import typing as th
from tap_shopify_beta.types.money_v2 import MoneyV2Type
from tap_shopify_beta.types.unit_price_measurement import UnitPriceMeasurementType

class UnitPriceType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("measurement", UnitPriceMeasurementType()),
            th.Property("price", MoneyV2Type())
        )
