from singer_sdk import typing as th

class SmsMarketingConsentType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("consentCollectedFrom", th.StringType),
            th.Property("consentUpdatedAt", th.DateTimeType),
            th.Property("marketingOptInLevel", th.StringType),
            th.Property("marketingState", th.StringType),
        )
