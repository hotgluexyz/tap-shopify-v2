from singer_sdk import typing as th

from tap_shopify_beta.types.marketing_event import MarketingEventType
from tap_shopify_beta.types.utm_parameter import UtmParameterType

class CustomerVisitType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("id", th.StringType),
            th.Property("landingPage", th.StringType),
            th.Property("landingPageHtml", th.StringType),
            th.Property("marketingEvent", MarketingEventType()),
            th.Property("occurredAt", th.StringType),
            th.Property("referralCode", th.StringType),
            th.Property("referralInfoHtml", th.StringType),
            th.Property("referrerUrl", th.StringType),
            th.Property("source", th.StringType),
            th.Property("sourceDescription", th.StringType),
            th.Property("sourceType", th.StringType),
            th.Property("utmParameters", UtmParameterType())
        )
