from singer_sdk import typing as th

from tap_shopify_beta.types.metafield_definition import MetafieldDefinitionType

class GenericMetafieldType(th.ObjectType):
    def __init__(self, *properties):
        super().__init__(
            th.Property("compareDigest", th.StringType),
            th.Property("createdAt", th.DateTimeType),
            th.Property("definition", MetafieldDefinitionType()),
            th.Property("description", th.StringType),
            th.Property("id", th.StringType),
            th.Property("jsonValue", th.StringType), # TODO: is this type right?
            th.Property("key", th.StringType),
            th.Property("legacyResourceid", th.StringType),
            th.Property("namespace", th.StringType),
            th.Property("type", th.StringType),
            th.Property("updatedAt", th.DateTimeType),
            th.Property("value", th.StringType),
            th.Property("ownerType", th.StringType),
            *properties
        )
                    