from singer_sdk import typing as th

from tap_shopify_beta.types.operation import OperationType
from tap_shopify_beta.types.price_list import PriceListType


class CatalogType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("id", th.StringType),
            th.Property("operations", th.ArrayType(OperationType())),
            th.Property("priceList", PriceListType()),
            # th.Property("hasCollection", th.BooleanType),
            th.Property("id", th.StringType),
            # th.Property("supportsFuturePublishing", th.BooleanType)
        )
