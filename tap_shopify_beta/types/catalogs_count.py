from singer_sdk import typing as th


class CatalogsCountType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("count", th.IntegerType),
            th.Property("precision", th.StringType)
        )