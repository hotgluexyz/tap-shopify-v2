from singer_sdk import typing as th

from tap_shopify_beta.types.market_web_presence_root_url import MarketWebPresenceRootUrlType
from tap_shopify_beta.types.shop_locale import ShopLocaleType

class MarketWebPresenceType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("alternateLocales", th.ArrayType(ShopLocaleType())),
            th.Property("defaultLocale", ShopLocaleType()),
            th.Property("id", th.StringType),
            th.Property("rootUrls", MarketWebPresenceRootUrlType()),
            th.Property("subfolderSuffix", th.StringType),                           
        )
                    