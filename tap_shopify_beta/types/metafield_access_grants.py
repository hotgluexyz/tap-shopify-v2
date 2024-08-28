from singer_sdk import typing as th

class MetafieldAccessGrantType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("access", th.StringType),
            th.Property("grantee", th.StringType),
        )
                            