from singer_sdk import typing as th

from tap_shopify_beta.types.location import LocationType

class FulfillmentType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("id", th.StringType),
            th.Property("createdAt", th.DateTimeType),
            th.Property("deliveredAt", th.DateTimeType),
            th.Property("displayStatus", th.StringType),
            th.Property("estimatedDeliveryAt", th.DateTimeType),
            th.Property("inTransitAt", th.DateTimeType),
            th.Property("legacyResourceId", th.StringType),
            th.Property("location", LocationType()),
            th.Property("name", th.StringType),
            th.Property("order", th.ObjectType(
                th.Property("id", th.StringType)
            )),
            th.Property("originAddress", th.ObjectType(
                th.Property("address1", th.StringType),
                th.Property("address2", th.StringType),
                th.Property("city", th.StringType),
                th.Property("countryCode", th.StringType),
                th.Property("provinceCode", th.StringType),
                th.Property("zip", th.StringType)
            )),
            th.Property("requiresShipping", th.BooleanType),
            th.Property("service", th.ObjectType(
                th.Property("id", th.StringType)
            )),
            th.Property("status", th.StringType),
            th.Property("totalQuantity", th.IntegerType),
            th.Property("trackingInfo", th.ArrayType(th.ObjectType(
                th.Property("company", th.StringType),
                th.Property("number", th.StringType),
                th.Property("url", th.StringType),
            ))),
            th.Property("updatedAt", th.DateTimeType),
        )
