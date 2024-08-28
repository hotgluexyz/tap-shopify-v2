from singer_sdk import typing as th

from tap_shopify_beta.types.access_scope import AccessScopeType
from tap_shopify_beta.types.app_metafield import AppMetafieldType
from tap_shopify_beta.types.app_subscription import AppSubscriptionType
from tap_shopify_beta.types.publication import PublicationType

class AppInstallationType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("accessScopes", th.ArrayType(AccessScopeType())),
            th.Property("activeSubscriptions", th.ArrayType(AppSubscriptionType())),
            th.Property("id", th.StringType),
            th.Property("launchUrl", th.StringType),
            # th.Property("metafield", AppMetafieldType()),
            th.Property("publication", PublicationType()),
            th.Property("uninstallUrl", th.StringType)
        )