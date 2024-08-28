from singer_sdk import typing as th

from tap_shopify_beta.types.metafield_definition_type import MetafieldDefinitionTypeType
from tap_shopify_beta.types.metafield_definition_validation import MetafieldDefinitionValidationType

class StandardMetafieldDefinitionTemplateType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("description", th.StringType),
            th.Property("id", th.StringType),
            th.Property("key", th.StringType),
            th.Property("metafieldsCount", th.IntegerType),
            th.Property("name", th.StringType),
            th.Property("namespace", th.StringType),
            th.Property("ownerType", th.StringType),
            th.Property("type", MetafieldDefinitionTypeType()),
            th.Property("validations", th.ArrayType(MetafieldDefinitionValidationType())),
            th.Property("visibleToStorefrontApi", th.StringType),
        )
