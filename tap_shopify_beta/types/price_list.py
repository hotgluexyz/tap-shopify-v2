from singer_sdk import typing as th


class PriceListType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("currency", th.StringType),
            th.Property("fixedPricesCount", th.StringType),
            th.Property("id", th.StringType),
            th.Property("name", th.StringType),
            th.Property("parent", th.ObjectType(
                th.Property("adjustment", th.ObjectType(
                    th.Property("type", th.StringType),
                    th.Property("value", th.IntegerType)
                )),
                th.Property("settings", th.ObjectType(
                    th.Property("compareAtMode", th.StringType)
                )),
            ))
        )
                    