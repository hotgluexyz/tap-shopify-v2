from singer_sdk import typing as th

from tap_shopify_beta.types.catalog import CatalogType


class PublicationType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("autoPublish", th.BooleanType),
            th.Property("catalog", CatalogType()),
            th.Property("id", th.StringType),
            th.Property("supportsFuturePublishing", th.BooleanType),
            # th.Property("hasCollection", th.BooleanType),
            th.Property("operation", th.StringType)
        )
                    