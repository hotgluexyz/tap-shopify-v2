from singer_sdk import typing as th

from tap_shopify_beta.types.count import CountType
from tap_shopify_beta.types.market_currency_settings import MarketCurrencySettingsType
from tap_shopify_beta.types.market_metafield import MarketMetafieldType
from tap_shopify_beta.types.market_web_presence import MarketWebPresenceType

class MarketType(th.ObjectType):
    def __init__(self):
        super().__init__(
            # th.Property("catalogsCount", CatalogsCountType()),
            th.Property("currencySettings", MarketCurrencySettingsType()),
            th.Property("enabled", th.BooleanType),
            th.Property("handle", th.StringType),
            th.Property("id", th.StringType),
            # th.Property("metafield", MarketMetafieldType()),
            th.Property("name", th.StringType),
            th.Property("primary", th.BooleanType),
            th.Property("webPresence", MarketWebPresenceType()),
        )