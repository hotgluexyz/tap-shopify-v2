from singer_sdk import typing as th

class AccessScopeType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("description", th.StringType),
            th.Property("handle", th.StringType)
        )
