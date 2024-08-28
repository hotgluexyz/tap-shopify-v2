from singer_sdk import typing as th

class NavigationItemType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("id", th.StringType),
            th.Property("title", th.StringType),
            th.Property("url", th.StringType)
        )
