from singer_sdk import typing as th


class OperationType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("id", th.StringType),
            th.Property("processedRowCount", th.IntegerType),
            th.Property("rowCount", th.ObjectType(
                th.Property("count", th.IntegerType),
                th.Property("exceedsMax", th.BooleanType)
            )),
            th.Property("status", th.StringType)
        )