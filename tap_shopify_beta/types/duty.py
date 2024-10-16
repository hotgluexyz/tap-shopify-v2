from singer_sdk import typing as th

from tap_shopify_beta.types.money_bag import MoneyBagType
from tap_shopify_beta.types.tax_line import TaxLineType


class DutyType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("countryCodeOfOrigin", th.StringType),
            th.Property("harmonizedSystemCode", th.StringType),
            th.Property("id", th.StringType),
            th.Property("price", MoneyBagType()),
            th.Property("taxLines", th.ArrayType(TaxLineType())),
        )
