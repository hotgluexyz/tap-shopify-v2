from singer_sdk import typing as th

from tap_shopify_beta.types.market_web_presence_root_url import MarketWebPresenceRootUrlType
from tap_shopify_beta.types.shop_locale import ShopLocaleType

class MarketWebPresenceType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("alternateLocales", th.ArrayType(th.ObjectType(
                th.Property("locale", th.StringType),
                th.Property("marketWebPresences", th.ArrayType(th.ObjectType(
                    th.Property("domain", th.ObjectType(
                        th.Property("host", th.StringType),
                        th.Property("id", th.StringType),
                        th.Property("localization", th.ObjectType(
                            th.Property("alternateLocales", th.ArrayType(th.StringType)),
                            th.Property("country", th.StringType),
                            th.Property("defaultLocale", th.StringType),
                        )),
                        th.Property("sslEnabled", th.BooleanType),
                        th.Property("url", th.StringType),
                    )),
                    th.Property("id", th.StringType),
                    th.Property("rootUrls", th.ObjectType(
                        th.Property("locale", th.StringType),
                        th.Property("url", th.StringType)
                    )),
                    th.Property("subfolderSuffix", th.StringType),
                ))),
                th.Property("name", th.StringType),
                th.Property("primary", th.BooleanType),
                th.Property("published", th.BooleanType),
            ))),
            th.Property("defaultLocale", th.ObjectType(
                th.Property("locale", th.StringType),
                th.Property("name", th.StringType),
                th.Property("primary", th.BooleanType),
                th.Property("published", th.BooleanType)
            )),
            th.Property("id", th.StringType),
            th.Property("rootUrls", MarketWebPresenceRootUrlType()),
            th.Property("subfolderSuffix", th.StringType),                           
        )
                    