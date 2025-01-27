from singer_sdk import typing as th
from tap_shopify_beta.types.app_feedback import AppFeedbackType
from tap_shopify_beta.types.count import CountType
from tap_shopify_beta.types.money_v2 import MoneyV2Type
from tap_shopify_beta.types.taxonomy_category import TaxonomyCategoryType
from tap_shopify_beta.types.product_option import ProductOptionType
from tap_shopify_beta.types.translation import TranslationType

class ProductType(th.ObjectType):
    def __init__(self):
        super().__init__(
            # th.Property("category", TaxonomyCategoryType()),
            # th.Property("combinedListingRole", th.StringType),
            th.Property("compareAtPriceRange", th.ObjectType(
                th.Property("maxVariantCompareAtPrice", MoneyV2Type()),
                th.Property("minVariantCompareAtPrice", MoneyV2Type()),
            )),
            th.Property("createdAt", th.DateTimeType),
            th.Property("defaultCursor", th.StringType),
            th.Property("description", th.StringType),
            th.Property("descriptionHtml", th.StringType),
            th.Property("feedback", th.ObjectType(
                th.Property("details", th.ArrayType(AppFeedbackType())),
                th.Property("summary", th.StringType),
            )),
            th.Property("giftCardTemplateSuffix", th.StringType),
            th.Property("handle", th.StringType),
            th.Property("hasOnlyDefaultVariant", th.BooleanType),
            th.Property("hasOutOfStockVariants", th.BooleanType),
            th.Property("hasVariantsThatRequiresComponents", th.BooleanType),
            th.Property("id", th.StringType),
            # th.Property("inCollection", th.BooleanType),
            th.Property("isGiftCard", th.BooleanType),
            th.Property("legacyResourceId", th.StringType),
            # th.Property("mediaCount", CountType()),
            th.Property("onlineStorePreviewUrl", th.StringType),
            th.Property("onlineStoreUrl", th.StringType),
            th.Property("options", th.ArrayType(ProductOptionType())),
            th.Property("priceRangeV2", th.ObjectType(
                th.Property("maxVariantPrice", MoneyV2Type()),
                th.Property("minVariantPrice", MoneyV2Type()),
            )),
            th.Property("productType", th.StringType),
            th.Property("publishedAt", th.StringType),
            # th.Property("publishedOnPublication", th.BooleanType),
            th.Property("requiresSellingPlan", th.BooleanType),
            # th.Property("sellingPlanGroupsCount", CountType()),
            th.Property("seo", th.ObjectType(
                th.Property("description", th.StringType),
                th.Property("title", th.StringType),
            )),
            th.Property("status", th.StringType),
            th.Property("tags", th.ArrayType(th.StringType)),
            th.Property("templateSuffix", th.StringType),
            th.Property("title", th.StringType),
            th.Property("totalInventory", th.IntegerType),
            th.Property("tracksInventory", th.BooleanType),
            # th.Property("translations", th.ArrayType(TranslationType())),
            th.Property("updatedAt", th.DateTimeType),
            # th.Property("variantsCount", CountType()),
            th.Property("vendor", th.StringType),
        )
