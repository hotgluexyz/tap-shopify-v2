from singer_sdk import typing as th


class MarketWebPresenceRootUrlType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("locale", th.StringType),
            th.Property("url", th.StringType)
        )                       
                    