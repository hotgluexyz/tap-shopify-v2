from singer_sdk import typing as th


class CustomAttributesType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("key", th.StringType),
            th.Property("value", th.StringType)
        )
