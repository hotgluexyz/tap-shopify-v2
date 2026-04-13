from hotglue_singer_sdk import typing as th


class LinkType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("label", th.StringType),
            # th.Property("translations", th.ArrayType(TranslationType())),
            th.Property("url", th.StringType)
        )
                    