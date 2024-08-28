from singer_sdk import typing as th

class PrivateMetafieldType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("createdAt", th.DateTimeType),
            th.Property("id", th.StringType),
            th.Property("key", th.StringType),
            th.Property("namespace", th.StringType),
            th.Property("updatedAt", th.DateTimeType),
            th.Property("value", th.StringType),
            th.Property("valueType", th.StringType),
        )