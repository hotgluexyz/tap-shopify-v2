from singer_sdk import typing as th


class ShopLocaleType(th.StringType):
    pass
    # def __init__(self):
    #     super().__init__(
    #         th.Property("locale", th.StringType),
    #         th.Property("marketWebPresences", th.ArrayType(th.ObjectType(  # DONT SUBSTITUTE for MarketWebPresenceType to avoid circular import/infinite loop
    #             th.Property("domain", th.StringType),
    #             th.Property("id", th.StringType),
    #             th.Property("rootUrls", th.ObjectType(
    #                 th.Property("locale", th.StringType),
    #                 th.Property("url", th.StringType)
    #             )),
    #             th.Property("subfolderSuffix", th.StringType),
    #         ))),
    #         th.Property("name", th.StringType),
    #         th.Property("primary", th.BooleanType),
    #         th.Property("published", th.BooleanType)
    #     )