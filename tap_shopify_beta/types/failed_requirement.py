from singer_sdk import typing as th

from tap_shopify_beta.types.navigation_item import NavigationItemType

class FailedRequirementType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("action", NavigationItemType()),
            th.Property("message", th.StringType)
        )
