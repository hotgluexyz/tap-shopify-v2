from singer_sdk import typing as th

from tap_shopify_beta.types.metafield_definition_type import MetafieldDefinitionTypeType
from tap_shopify_beta.types.metafield_definition_validation import MetafieldDefinitionValidationType
from tap_shopify_beta.types.standard_metafield_definition_template import StandardMetafieldDefinitionTemplateType
from tap_shopify_beta.types.metafield_access import MetafieldAccessType
from tap_shopify_beta.types.metafield_definition_constraints import MetafieldDefinitionConstraintsType

class MetafieldDefinitionType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("access", MetafieldAccessType()),
            th.Property("constraints", MetafieldDefinitionConstraintsType()),
            th.Property("description", th.StringType),
            th.Property("id", th.StringType),
            th.Property("key", th.StringType),
            th.Property("metafieldsCount", th.IntegerType),
            th.Property("name", th.StringType),
            th.Property("namespace", th.StringType),
            th.Property("ownerType", th.StringType),
            th.Property("pinnedPosition", th.IntegerType),
            th.Property("standardTemplate", StandardMetafieldDefinitionTemplateType()),
            th.Property("type", MetafieldDefinitionTypeType()),
            th.Property("useAsCollectionCondition", th.BooleanType),
            th.Property("validationStatus", th.StringType),
            th.Property("validations", th.ArrayType(MetafieldDefinitionValidationType())),
        )
                        