from singer_sdk import typing as th
from .metafield_access_grants import MetafieldAccessGrantType

class MetafieldAccessType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("admin", th.StringType),
            th.Property("customerAccount", th.StringType),
            th.Property("grants", th.ArrayType(MetafieldAccessGrantType())),
            th.Property("storefront", th.StringType)
        )
