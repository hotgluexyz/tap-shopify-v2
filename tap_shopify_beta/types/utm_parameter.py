from singer_sdk import typing as th


class UtmParameterType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("campaign", th.StringType),
            th.Property("content", th.StringType),
            th.Property("medium", th.StringType),
            th.Property("source", th.StringType),
            th.Property("term", th.StringType)
        )