from singer_sdk import typing as th

from tap_shopify_beta.types.image import ImageType
from tap_shopify_beta.types.translation import TranslationType


class ProductOptionValueType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("hasVariants", th.BooleanType),
            th.Property("id", th.StringType),
            th.Property("linkedMetafieldValue", th.StringType),
            th.Property("name", th.StringType),
            th.Property("swatch", th.ObjectType(
                th.Property("color", th.StringType),
                th.Property("image", ImageType()),
            )),
            th.Property("translations", th.ArrayType(TranslationType())),
        )
