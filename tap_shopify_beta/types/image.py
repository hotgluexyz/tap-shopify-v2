from singer_sdk import typing as th


class ImageType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("altText", th.StringType),
            th.Property("height", th.IntegerType),
            th.Property("id", th.StringType),
            # th.Property("metafield", ImageMetafieldType()),
            th.Property("url", th.StringType),
            th.Property("width", th.IntegerType)
        )
