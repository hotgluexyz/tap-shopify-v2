from singer_sdk import typing as th

from tap_shopify_beta.types.metafield_definition_supported_validation import MetafieldDefinitionSupportedValidationType

class MetafieldDefinitionTypeType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("category", th.StringType),
            th.Property("name", th.StringType),
            th.Property("supportedValidations", th.ArrayType(MetafieldDefinitionSupportedValidationType())),
            th.Property("supportsDefinitionMigrations", th.BooleanType)
        )