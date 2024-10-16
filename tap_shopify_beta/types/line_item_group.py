from singer_sdk import typing as th

from tap_shopify_beta.types.custom_attributes import CustomAttributesType


class LineItemGroupType(th.ObjectType):
    def __init__(self):
        super().__init__(
            # th.Property("customAttributes", CustomAttributesType()),
            th.Property("id", th.StringType),
            th.Property("quantity", th.IntegerType),
            th.Property("title", th.StringType),
            th.Property("variantId", th.StringType),
            th.Property("variantSku", th.StringType),
        )
