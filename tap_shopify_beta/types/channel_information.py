from singer_sdk import typing as th

from tap_shopify_beta.types.app import AppType

class ChannelInformationType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("app", AppType()),
            th.Property("channelDefinition", th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("channelName", th.StringType),
                th.Property("handle", th.StringType), 
                th.Property("isMarketplace", th.BooleanType),
                th.Property("subChannelName", th.StringType),
                th.Property("svgIcon", th.StringType),
            )),
            th.Property("channelId", th.StringType),
            th.Property("id", th.StringType),
        )
