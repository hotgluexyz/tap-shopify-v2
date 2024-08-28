from singer_sdk import typing as th


class UserErrorType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("field", th.ArrayType(th.StringType)),
            th.Property("message", th.StringType)
        )
