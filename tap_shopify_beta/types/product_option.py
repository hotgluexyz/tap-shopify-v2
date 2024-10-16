from singer_sdk import typing as th

from tap_shopify_beta.types.product_option_value import ProductOptionValueType
from tap_shopify_beta.types.translation import TranslationType

class ProductOptionType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("id", th.StringType),
            # th.Property("linkedMetafield", th.ObjectType(
            #     th.Property("key", th.StringType),
            #     th.Property("namespace", th.StringType),
            # )),
            th.Property("name", th.BooleanType),
            # th.Property("optionValues", th.ArrayType(ProductOptionValueType())),
            th.Property("position", th.IntegerType),
            # th.Property("translations", th.ArrayType(TranslationType())),
            th.Property("values", th.ArrayType(th.StringType)),
        )
