from singer_sdk import typing as th

from tap_shopify_beta.types.app import AppType

class MarketingEventType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("app", AppType()),
            th.Property("channelHandle", th.StringType),
            th.Property("description", th.StringType),
            th.Property("endedAt", th.DateTimeType),
            th.Property("id", th.StringType),
            # th.Property("legacyResourceid", th.IntegerType),
            th.Property("manageUrl", th.StringType),
            th.Property("marketingChannelType", th.StringType),
            th.Property("previewUrl", th.StringType),
            th.Property("remoteId", th.StringType),
            th.Property("scheduledToEndAt", th.DateTimeType),
            th.Property("sourceAndMedium", th.StringType),
            th.Property("startedAt", th.DateTimeType),
            th.Property("type", th.StringType),
            th.Property("utmCampaign", th.StringType),
            th.Property("utmMedium", th.StringType),
            th.Property("utmSource", th.StringType)
        )