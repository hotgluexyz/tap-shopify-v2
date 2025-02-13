from singer_sdk import typing as th

from tap_shopify_beta.types.image_metafield import ImageMetafieldType

class ImageType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("altText", th.StringType),
            th.Property("height", th.IntegerType),
            th.Property("id", th.StringType),
            # th.Property("metafield", ImageMetafieldType()),
            th.Property("url", th.StringType),
            th.Property("width", th.IntegerType),
            th.Property("originalSrc", th.StringType)
        )
