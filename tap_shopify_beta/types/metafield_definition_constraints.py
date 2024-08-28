from singer_sdk import typing as th

class MetafieldDefinitionConstraintsType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("key", th.StringType)
        )