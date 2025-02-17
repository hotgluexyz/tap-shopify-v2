from singer_sdk import typing as th

from tap_shopify_beta.types.access_scope import AccessScopeType
from tap_shopify_beta.types.image import ImageType

class AppType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("id", th.StringType),
            th.Property("apiKey", th.StringType),
            th.Property("appStoreAppUrl", th.StringType),
            th.Property("appStoreDeveloperUrl", th.StringType),
            th.Property("banner", ImageType()),
            th.Property("description", th.StringType),
            th.Property("developerName", th.StringType),
            th.Property("developerType", th.StringType),
            th.Property("embedded", th.BooleanType),
            th.Property("features", th.ArrayType(th.StringType)),
            th.Property("icon", ImageType()),
            th.Property("id", th.StringType),
            th.Property("installUrl", th.StringType),
            th.Property("isPostPurchaseAppInUse", th.BooleanType),
            th.Property("previouslyInstalled", th.BooleanType),
            th.Property("pricingDetails", th.StringType),
            th.Property("pricingDetailsSummary", th.StringType),
            th.Property("privacyPolicyUrl", th.StringType),
            th.Property("publicCategory", th.StringType),
            th.Property("published", th.BooleanType),
            th.Property("requestedAccessScopes", th.ArrayType(AccessScopeType())),
            th.Property("shopifyDeveloped", th.BooleanType),
            th.Property("title", th.StringType),
            th.Property("uninstallMessage", th.StringType),
            th.Property("webhookApiVersion", th.StringType)
        )