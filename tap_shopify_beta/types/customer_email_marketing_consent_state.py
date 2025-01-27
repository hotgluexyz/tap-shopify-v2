from singer_sdk import typing as th

from tap_shopify_beta.types.customer import CustomerType

class CustomerEmailMarketingConsentStateType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("consentUpdatedAt", th.DateTimeType),
            th.Property("marketingOptInLevel", th.StringType),
            th.Property("marketingState", th.StringType),
        )
