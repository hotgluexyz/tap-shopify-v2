from singer_sdk import typing as th

from tap_shopify_beta.types.contract import ContractType
from tap_shopify_beta.types.duty import DutyType
from tap_shopify_beta.types.custom_attributes import CustomAttributesType
from tap_shopify_beta.types.discount_allocations import DiscountAllocationsType
from tap_shopify_beta.types.image import ImageType
from tap_shopify_beta.types.money_bag import MoneyBagType
from tap_shopify_beta.types.line_item_group import LineItemGroupType
from tap_shopify_beta.types.product import ProductType
from tap_shopify_beta.types.staff_member import StaffMemberType
from tap_shopify_beta.types.tax_line import TaxLineType


class LineItemNodeType(th.ObjectType):
    def __init__(self):
        super().__init__(
            # th.Property("contract", ContractType()),
            th.Property("contract", th.ObjectType(
                th.Property("id", th.StringType)
            )),
            th.Property("currentQuantity", th.IntegerType),
            # th.Property("customAttributes", th.ArrayType(CustomAttributesType())),
            # th.Property("discountAllocations", th.ArrayType(DiscountAllocationsType())),
            th.Property("discountedTotalSet", MoneyBagType()),
            # th.Property("discountedUnitPriceAfterAllDiscountsSet", MoneyBagType()),
            th.Property("discountedUnitPriceSet", MoneyBagType()),
            # th.Property("duties", th.ArrayType(DutyType())),
            th.Property("id", th.StringType),
            th.Property("image", ImageType()),
            # th.Property("isGiftCard", th.BooleanType),
            th.Property("lineItemGroup", LineItemGroupType()),
            th.Property("merchantEditable", th.BooleanType),
            th.Property("name", th.StringType),
            th.Property("nonFulfillableQuantity", th.IntegerType),
            th.Property("originalTotalSet", MoneyBagType()),
            th.Property("originalUnitPriceSet", MoneyBagType()),
            th.Property("product", th.ObjectType(
                th.Property("id", th.StringType)
            )),
            # th.Property("product", ProductType()),
            th.Property("quantity", th.IntegerType),
            th.Property("refundableQuantity", th.IntegerType),
            th.Property("requiresShipping", th.BooleanType),
            th.Property("restockable", th.BooleanType),
            th.Property("sellingPlan", th.ObjectType(
                th.Property("name", th.StringType),
                th.Property("sellingPlanId", th.StringType),
            )),
            th.Property("sku", th.StringType),
            # th.Property("staffMember", StaffMemberType()),
            th.Property("taxable", th.BooleanType),
            th.Property("taxLines", th.ArrayType(TaxLineType())),
            th.Property("title", th.StringType),
            th.Property("totalDiscountSet", MoneyBagType()),
            th.Property("unfulfilledDiscountedTotalSet", MoneyBagType()),
            th.Property("unfulfilledOriginalTotalSet", MoneyBagType()),
            th.Property("unfulfilledQuantity", th.IntegerType),
            th.Property("variant", th.ObjectType(
                th.Property("id", th.StringType)
            )),
            th.Property("variantTitle", th.StringType),
            th.Property("vendor", th.StringType),
        )
