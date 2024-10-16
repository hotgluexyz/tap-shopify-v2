from singer_sdk import typing as th

class PricingPercentageValueType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("percentage", th.StringType),
        )
