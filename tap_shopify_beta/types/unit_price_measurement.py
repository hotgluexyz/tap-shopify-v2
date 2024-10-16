from singer_sdk import typing as th

class UnitPriceMeasurementType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("referenceUnit", th.StringType),
            th.Property("referenceValue", th.IntegerType)
        )
