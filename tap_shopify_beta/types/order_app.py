from singer_sdk import typing as th

from tap_shopify_beta.types.image import ImageType

class OrderAppType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("id", th.StringType),
            th.Property("name", th.StringType),
            th.Property("icon", ImageType())
        )