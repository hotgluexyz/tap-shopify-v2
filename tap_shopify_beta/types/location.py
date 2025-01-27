from singer_sdk import typing as th

class LocationType(th.ObjectType):
    def __init__(self):
        super().__init__(
                            th.Property("activatable", th.BooleanType),
                            th.Property("address", th.ObjectType(
                                th.Property("address1", th.StringType),
                                th.Property("address2", th.StringType),
                                th.Property("city", th.StringType),
                                th.Property("country", th.StringType),
                                th.Property("countryCode", th.StringType),
                                th.Property("formatted", th.ArrayType(th.StringType)),
                                th.Property("latitude", th.NumberType),
                                th.Property("longitude", th.NumberType),
                                th.Property("phone", th.StringType),
                                th.Property("province", th.StringType),
                                th.Property("provinceCode", th.StringType),
                                th.Property("zip", th.StringType),
                            )),
                            th.Property("addressVerified", th.BooleanType),
                            th.Property("createdAt", th.DateTimeType),
                            th.Property("deactivatable", th.BooleanType),
                            th.Property("deactivatedAt", th.StringType),
                            th.Property("deletable", th.BooleanType),
                            th.Property("fulfillmentService", th.ObjectType(
                                th.Property("callbackUrl", th.StringType),
                                th.Property("handle", th.StringType),
                                th.Property("id", th.StringType),
                                th.Property("inventoryManagement", th.BooleanType),
                                th.Property("location", th.ObjectType(
                                    th.Property("id", th.StringType)
                                )),
                                th.Property("permitsSkuSharing", th.BooleanType),
                                th.Property("serviceName", th.StringType),
                                th.Property("type", th.StringType),
                            )),
                            th.Property("fulfillsOnlineOrders", th.BooleanType),
                            th.Property("hasActiveInventory", th.BooleanType),
                            th.Property("hasUnfulfilledOrders", th.BooleanType),
                            th.Property("id", th.StringType),
                            th.Property("isActive", th.BooleanType),
                            th.Property("isFulfillmentService", th.BooleanType),
                            th.Property("legacyResourceId", th.StringType),
                            th.Property("name", th.StringType),
                            th.Property("shipsInventory", th.BooleanType),
                            th.Property("updatedAt", th.DateTimeType)
                        )