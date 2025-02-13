from singer_sdk import typing as th

class DisputeType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("id", th.StringType),
            th.Property("initiatedAs", th.StringType),
            th.Property("status", th.StringType),
        )
