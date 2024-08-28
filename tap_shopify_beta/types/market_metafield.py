from singer_sdk import typing as th

from tap_shopify_beta.types.generic_metafield import GenericMetafieldType
from tap_shopify_beta.types.owner_metafield import OwnerMetafieldType

class MarketMetafieldType(GenericMetafieldType):
    def __init__(self):
        super().__init__(
            th.Property("owner", OwnerMetafieldType())
        )
                    