from singer_sdk import typing as th

class MetafieldDefinitionSupportedValidationType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("name", th.StringType),
            th.Property("type", th.StringType)
        )