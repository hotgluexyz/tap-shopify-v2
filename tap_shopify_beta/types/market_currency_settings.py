from singer_sdk import typing as th

from tap_shopify_beta.types.currency_settings import CurrencySettingsType

class MarketCurrencySettingsType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("baseCurrency", CurrencySettingsType()),
            th.Property("localCurrencies", th.StringType)
        )