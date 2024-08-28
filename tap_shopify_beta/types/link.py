from singer_sdk import typing as th

from tap_shopify_beta.types.translation import TranslationType

class LinkType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("label", th.StringType),
            # th.Property("translations", th.ArrayType(TranslationType())),
            th.Property("url", th.StringType)
        )
                    