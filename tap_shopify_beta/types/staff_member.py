from singer_sdk import typing as th

from tap_shopify_beta.types.image import ImageType


class StaffMemberType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("active", th.BooleanType),
            th.Property("avatar", ImageType()),
            th.Property("email", th.StringType),
            th.Property("exists", th.BooleanType),
            th.Property("firstName", th.StringType),
            th.Property("id", th.StringType),
            th.Property("initials", th.ArrayType(th.StringType)),
            th.Property("isShopOwner", th.BooleanType),
            th.Property("lastName", th.StringType),
            th.Property("locale", th.StringType),
            th.Property("name", th.StringType),
            th.Property("phone", th.StringType),
            th.Property("privateData", th.ObjectType(
                th.Property("accountSettingsUrl", th.StringType),
                th.Property("createdAt", th.DateTimeType),
            )),
        )
