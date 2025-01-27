from singer_sdk import typing as th


class MailingAddressType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("address1", th.StringType),
            th.Property("address2", th.StringType),
            th.Property("city", th.StringType),
            th.Property("company", th.StringType),
            th.Property("coordinatesValidated", th.BooleanType),
            th.Property("country", th.StringType),
            th.Property("countryCodeV2", th.StringType),
            th.Property("firstName", th.StringType),
            th.Property("formatted", th.ArrayType(th.StringType)),
            th.Property("formattedArea", th.StringType),
            th.Property("formattedArea", th.StringType),
            th.Property("lastName", th.StringType),
            th.Property("latitude", th.NumberType),
            th.Property("longitude", th.NumberType),
            th.Property("name", th.StringType),
            th.Property("phone", th.StringType),
            th.Property("province", th.StringType),
            th.Property("provinceCode", th.StringType),
            th.Property("timeZone", th.StringType),
            th.Property("zip", th.StringType),
        )
