from singer_sdk import typing as th


class TaxonomyCategoryType(th.ObjectType):
    def __init__(self):
        super().__init__(
            th.Property("ancestorIds", th.ArrayType(th.StringType)),
            th.Property("childrenIds", th.ArrayType(th.StringType)),
            th.Property("fullName", th.StringType),
            th.Property("id", th.StringType),
            th.Property("isArchived", th.BooleanType),
            th.Property("isLeaf", th.BooleanType),
            th.Property("isRoot", th.BooleanType),
            th.Property("level", th.IntegerType),
            th.Property("name", th.StringType),
            th.Property("parentId", th.StringType),
        )
