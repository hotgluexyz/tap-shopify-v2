"""Stream type classes for tap-shopify-beta."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th

from tap_shopify_beta.client import shopifyStream
from tap_shopify_beta.client_bulk import shopifyBulkStream
from tap_shopify_beta.client_gql import shopifyGqlStream


MoneyBag = th.ObjectType(
    th.Property(
        "presentmentMoney",
        th.ObjectType(
            th.Property("amount", th.StringType),
            th.Property("currencyCode", th.StringType),
        ),
    ),
    th.Property(
        "shopMoney",
        th.ObjectType(
            th.Property("amount", th.StringType),
            th.Property("currencyCode", th.StringType),
        ),
    ),
)


class ProductsStream(shopifyBulkStream):
    """Define product stream."""

    name = "products"
    primary_keys = ["id", "updatedAt"]
    query_name = "products"
    replication_key = "updatedAt"

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("description", th.StringType),
        th.Property("descriptionHtml", th.StringType),
        th.Property(
            "featuredImage",
            th.ObjectType(
                th.Property("id", th.StringType), th.Property("altText", th.StringType)
            ),
        ),
        th.Property("giftCardTemplateSuffix", th.StringType),
        th.Property("handle", th.StringType),
        th.Property("hasOnlyDefaultVariant", th.BooleanType),
        th.Property("hasOutOfStockVariants", th.BooleanType),
        th.Property("isGiftCard", th.BooleanType),
        th.Property("legacyResourceId", th.StringType),
        th.Property("mediaCount", th.IntegerType),
        th.Property("onlineStorePreviewUrl", th.StringType),
        th.Property("onlineStoreUrl", th.StringType),
        th.Property(
            "options",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("name", th.StringType),
                    th.Property("position", th.IntegerType),
                    th.Property("values", th.ArrayType(th.StringType)),
                )
            ),
        ),
        th.Property(
            "priceRangeV2",
            th.ObjectType(
                th.Property(
                    "maxVariantPrice",
                    th.ObjectType(
                        th.Property("amount", th.StringType),
                        th.Property("currencyCode", th.StringType),
                    ),
                ),
                th.Property(
                    "minVariantPrice",
                    th.ObjectType(
                        th.Property("amount", th.StringType),
                        th.Property("currencyCode", th.StringType),
                    ),
                ),
            ),
        ),
        th.Property("productType", th.StringType),
        th.Property("publishedAt", th.DateTimeType),
        th.Property("requiresSellingPlan", th.BooleanType),
        th.Property("sellingPlanGroupCount", th.IntegerType),
        th.Property(
            "seo",
            th.ObjectType(
                th.Property("title", th.StringType),
                th.Property("description", th.StringType),
            ),
        ),
        th.Property("status", th.StringType),
        th.Property("templateSuffix", th.StringType),
        th.Property("title", th.StringType),
        th.Property("totalInventory", th.IntegerType),
        th.Property("totalVariants", th.IntegerType),
        th.Property("tracksInventory", th.BooleanType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property("vendor", th.StringType),
    ).to_dict()


class VariantsStream(shopifyBulkStream):
    """Define variant stream."""

    name = "variants"
    primary_keys = ["id", "updatedAt"]
    query_name = "productVariants"
    replication_key = "updatedAt"

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("availableForSale", th.BooleanType),
        th.Property("barcode", th.StringType),
        th.Property("compareAtPrice", th.StringType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("displayName", th.StringType),
        th.Property(
            "fulfillmentService",
            th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("callbackUrl", th.StringType),
                th.Property("fulfillmentOrdersOptIn", th.BooleanType),
                th.Property("handle", th.StringType),
                th.Property("inventoryManagement", th.BooleanType),
                th.Property(
                    "location", th.ObjectType(th.Property("id", th.StringType))
                ),
                th.Property("productBased", th.BooleanType),
                th.Property("serviceName", th.StringType),
                th.Property(
                    "shippingMethods",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("code", th.StringType),
                            th.Property("label", th.StringType),
                        )
                    ),
                    th.Property("type", th.StringType),
                ),
            ),
        ),
        th.Property(
            "fulfillmentServiceEditable",
            th.ObjectType(
                th.Property("locked", th.BooleanType),
                th.Property("reason", th.StringType),
            ),
        ),
        th.Property(
            "image",
            th.ObjectType(
                th.Property("id", th.StringType), th.Property("altText", th.StringType)
            ),
        ),
        th.Property("inventoryItem", th.ObjectType(th.Property("id", th.StringType))),
        th.Property("inventoryPolicy", th.StringType),
        th.Property("inventoryQuantity", th.IntegerType),
        th.Property("legacyResourceId", th.StringType),
        th.Property("position", th.IntegerType),
        th.Property("price", th.StringType),
        th.Property("product", th.ObjectType(th.Property("id", th.StringType))),
        th.Property(
            "selectedOptions",
            th.ArrayType(
                th.ObjectType(
                    th.Property("name", th.StringType),
                    th.Property("value", th.StringType),
                )
            ),
        ),
        th.Property("sellingPlanGroupCount", th.IntegerType),
        th.Property("sku", th.StringType),
        th.Property("taxable", th.BooleanType),
        th.Property("title", th.StringType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property("weight", th.NumberType),
        th.Property("weightUnit", th.StringType),
    ).to_dict()


class OrdersStream(shopifyGqlStream):
    """Define orders stream."""

    name = "orders"
    primary_keys = ["id", "updatedAt"]
    query_name = "orders"
    replication_key = "updatedAt"

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property(
            "billingAddress",
            th.ObjectType(
                th.Property("id", th.StringType),
            ),
        ),
        th.Property("billingAddressMatchesShippingAddress", th.BooleanType),
        th.Property("cancelledAt", th.DateTimeType),
        th.Property("cancelReason", th.StringType),
        th.Property("canMarkAsPaid", th.BooleanType),
        th.Property("canNotifyCustomer", th.BooleanType),
        th.Property("capturable", th.BooleanType),
        th.Property("cartDiscountAmountSet", MoneyBag),
        th.Property("clientIp", th.StringType),
        th.Property("closed", th.BooleanType),
        th.Property("closedAt", th.DateTimeType),
        th.Property("confirmed", th.BooleanType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("currencyCode", th.StringType),
        th.Property("currentCartDiscountAmountSet", MoneyBag),
        th.Property("currentSubtotalLineItemsQuantity", th.IntegerType),
        th.Property("currentSubtotalPriceSet", MoneyBag),
        th.Property(
            "currentTaxLines",
            th.ArrayType(
                th.ObjectType(
                    th.Property("channelLiable", th.StringType),
                    th.Property("priceSet", MoneyBag),
                    th.Property("rate", th.NumberType),
                    th.Property("ratePercentage", th.NumberType),
                    th.Property("title", th.StringType),
                )
            ),
        ),
        th.Property("currentTotalDiscountsSet", MoneyBag),
        th.Property("currentTotalDutiesSet", MoneyBag),
        th.Property("currentTotalPriceSet", MoneyBag),
        th.Property("currentTotalTaxSet", MoneyBag),
        th.Property("currentTotalWeight", th.StringType),
        th.Property(
            "customer",
            th.ObjectType(
                th.Property("id", th.StringType),
            ),
        ),
        th.Property("customerAcceptsMarketing", th.BooleanType),
        th.Property("customerLocale", th.StringType),
        th.Property("discountCode", th.StringType),
        th.Property(
            "displayAddress",
            th.ObjectType(
                th.Property("id", th.StringType),
            ),
        ),
        th.Property("displayFinancialStatus", th.StringType),
        th.Property("displayFulfillmentStatus", th.StringType),
        th.Property(
            "disputes",
            th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("initiatedAs", th.StringType),
                th.Property("status", th.StringType),
            ),
        ),
        th.Property("edited", th.BooleanType),
        th.Property("email", th.StringType),
        th.Property("estimatedTaxes", th.BooleanType),
        th.Property("fulfillable", th.BooleanType),
        th.Property(
            "fulfillments",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("inTransitAt", th.StringType),
                    th.Property("legacyResourceId", th.StringType),
                    th.Property(
                        "location", th.ObjectType(th.Property("id", th.StringType))
                    ),
                    th.Property("name", th.StringType),
                    th.Property("requiresShipping", th.BooleanType),
                    th.Property(
                        "service", th.ObjectType(th.Property("id", th.StringType))
                    ),
                    th.Property("status", th.StringType),
                    th.Property("totalQuantity", th.IntegerType),
                    th.Property(
                        "trackingInfo",
                        th.ObjectType(
                            th.Property("company", th.StringType),
                            th.Property("number", th.StringType),
                            th.Property("url", th.StringType),
                        ),
                    ),
                    th.Property("updatedAt", th.DateTimeType),
                )
            ),
        ),
        th.Property("fullyPaid", th.BooleanType),
        th.Property("hasTimelineComment", th.BooleanType),
        th.Property("legacyResourceId", th.StringType),
        th.Property("merchantEditable", th.ArrayType(th.StringType)),
        th.Property("name", th.StringType),
        th.Property("netPaymentSet", MoneyBag),
        th.Property("note", th.StringType),
        th.Property("originalTotalDutiesSet", MoneyBag),
        th.Property("originalTotalPriceSet", MoneyBag),
        th.Property("paymentGatewayNames", th.ArrayType(th.StringType)),
        th.Property("phone", th.StringType),
        th.Property("presentmentCurrencyCode", th.StringType),
        th.Property("processedAt", th.DateTimeType),
        th.Property("refundable", th.BooleanType),
        th.Property("refundDiscrepancySet", MoneyBag),
        th.Property(
            "refunds",
            th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("createdAt", th.DateTimeType),
                th.Property(
                    "duties",
                    th.ObjectType(
                        th.Property("amountSet", MoneyBag),
                    ),
                ),
                th.Property("legacyResourceId", th.StringType),
                th.Property("note", th.StringType),
                th.Property("totalRefundedSet", MoneyBag),
                th.Property("updatedAt", th.DateTimeType),
            ),
        ),
        th.Property("requiresShipping", th.BooleanType),
        th.Property("restockable", th.BooleanType),
        th.Property("riskLevel", th.StringType),
        th.Property(
            "risks",
            th.ArrayType(
                th.ObjectType(
                    th.Property("display", th.BooleanType),
                    th.Property("level", th.StringType),
                    th.Property("message", th.StringType),
                )
            ),
        ),
        th.Property("shippingAddress", th.ObjectType(th.Property("id", th.StringType))),
        th.Property(
            "shippingLine",
            th.ObjectType(
                th.Property("carrierIdentifier", th.StringType),
                th.Property("code", th.StringType),
                th.Property("custom", th.StringType),
                th.Property("deliveryCategory", th.StringType),
            ),
        ),
        th.Property("subtotalLineItemsQuantity", th.IntegerType),
        th.Property("subtotalPriceSet", MoneyBag),
        th.Property("taxesIncluded", th.BooleanType),
        th.Property(
            "taxLines",
            th.ArrayType(
                th.ObjectType(
                    th.Property("channelLiable", th.StringType),
                    th.Property("priceSet", MoneyBag),
                    th.Property("rate", th.NumberType),
                    th.Property("ratePercentage", th.NumberType),
                    th.Property("title", th.StringType),
                )
            ),
        ),
        th.Property("totalCapturableSet", MoneyBag),
        th.Property("totalDiscountsSet", MoneyBag),
        th.Property("totalOutstandingSet", MoneyBag),
        th.Property("totalPriceSet", MoneyBag),
        th.Property("totalReceivedSet", MoneyBag),
        th.Property("totalRefundedSet", MoneyBag),
        th.Property("totalRefundedShippingSet", MoneyBag),
        th.Property("totalShippingPriceSet", MoneyBag),
        th.Property("totalTaxSet", MoneyBag),
        th.Property("totalTipReceivedSet", MoneyBag),
        th.Property("totalWeight", th.StringType),
        th.Property(
            "transactions",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                )
            ),
        ),
        th.Property("unpaid", th.BooleanType),
        th.Property("updatedAt", th.DateTimeType),
    ).to_dict()


class ShopStream(shopifyGqlStream):
    """Define shop stream."""

    name = "shop"
    primary_keys = ["id"]
    query_name = "shop"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("contactEmail", th.StringType),
        th.Property(
            "countriesInShippingZones",
            th.ObjectType(
                th.Property("countryCodes", th.ArrayType(th.StringType)),
            ),
            th.Property("includeRestOfWorld", th.BooleanType),
        ),
        th.Property("currencyCode", th.StringType),
        th.Property(
            "currencyFormats",
            th.ObjectType(
                th.Property("moneyFormat", th.StringType),
                th.Property("moneyInEmailsFormat", th.StringType),
                th.Property("moneyWithCurrencyFormat", th.StringType),
                th.Property("moneyWithCurrencyInEmailsFormat", th.StringType),
            ),
        ),
        th.Property("customerAccounts", th.StringType),
        th.Property("description", th.StringType),
        th.Property(
            "domains",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("host", th.StringType),
                    th.Property("sslEnabled", th.BooleanType),
                    th.Property("url", th.StringType),
                )
            ),
        ),
        th.Property("email", th.StringType),
        th.Property("enabledPresentmentCurrencies", th.ArrayType(th.StringType)),
        th.Property(
            "features",
            th.ObjectType(
                th.Property("branding", th.StringType),
                th.Property("captcha", th.BooleanType),
                th.Property("captchaExternalDomains", th.BooleanType),
                th.Property("dynamicRemarketing", th.BooleanType),
                th.Property("giftCards", th.BooleanType),
                th.Property("harmonizedSystemCode", th.BooleanType),
                th.Property("internationalDomains", th.BooleanType),
                th.Property("internationalPriceOverrides", th.BooleanType),
                th.Property("internationalPriceRules", th.BooleanType),
                th.Property("reports", th.BooleanType),
                th.Property("sellsSubscriptions", th.BooleanType),
                th.Property("showMetrics", th.BooleanType),
            ),
        ),
        th.Property(
            "fulfillmentServices",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("callbackUrl", th.StringType),
                    th.Property("fulfillmentOrdersOptIn", th.BooleanType),
                    th.Property("handle", th.StringType),
                    th.Property("inventoryManagement", th.BooleanType),
                    th.Property(
                        "location",
                        th.ObjectType(
                            th.Property("id", th.StringType),
                        ),
                    ),
                    th.Property("productBased", th.BooleanType),
                    th.Property("serviceName", th.StringType),
                    th.Property("type", th.StringType),
                )
            ),
        ),
        th.Property("ianaTimezone", th.StringType),
        th.Property(
            "limitedPendingOrderCount",
            th.ObjectType(
                th.Property("atMax", th.BooleanType),
                th.Property("count", th.IntegerType),
            ),
        ),
        th.Property("myshopifyDomain", th.StringType),
        th.Property("name", th.StringType),
        th.Property(
            "navigationSettings",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("title", th.StringType),
                    th.Property("url", th.StringType),
                )
            ),
        ),
        th.Property("orderNumberFormatPrefix", th.StringType),
        th.Property("orderNumberFormatSuffix", th.StringType),
        th.Property(
            "navigationSettings",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("title", th.StringType),
                    th.Property("url", th.StringType),
                )
            ),
        ),
        th.Property(
            "primaryDomain",
            th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("host", th.StringType),
                th.Property("sslEnabled", th.BooleanType),
                th.Property("url", th.StringType),
            ),
        ),
        th.Property("taxesIncluded", th.BooleanType),
        th.Property("taxShipping", th.BooleanType),
        th.Property("timezoneAbbreviation", th.StringType),
        th.Property("timezoneOffset", th.StringType),
        th.Property("timezoneOffsetMinutes", th.IntegerType),
        th.Property("unitSystem", th.StringType),
        th.Property("url", th.StringType),
        th.Property("weightUnit", th.StringType),
    ).to_dict()

class InventoryItemsStream(shopifyGqlStream):
    """Define shop stream."""

    name = "inventory_items"
    primary_keys = ["id"]
    query_name = "inventoryItems"
    replication_key = 'updatedAt'

    schema = th.PropertiesList(
        th.Property('id',th.StringType),
        th.Property('countryCodeOfOrigin',th.StringType),
        th.Property('createdAt',th.DateTimeType),
        th.Property('duplicateSkuCount',th.IntegerType),
        th.Property('harmonizedSystemCode',th.StringType),
        th.Property('inventoryHistoryUrl',th.StringType),
        th.Property('legacyResourceId',th.StringType),
        th.Property('locationsCount',th.IntegerType),
        th.Property('provinceCodeOfOrigin',th.StringType),
        th.Property('requiresShipping',th.BooleanType),
        th.Property('sku',th.StringType),
        th.Property('tracked',th.BooleanType),
        th.Property('trackedEditable',th.ObjectType(
            th.Property('locked',th.BooleanType),
            th.Property('reason',th.StringType),
            )
        ),
        th.Property('unitCost',th.ObjectType(
            th.Property('amount',th.NumberType),
            th.Property('currencyCode',th.StringType),
            )
        ),
        th.Property('updatedAt',th.DateTimeType),
        th.Property('variant',th.ObjectType(
                th.Property('id',th.StringType),
                th.Property('availableForSale',th.BooleanType),
                th.Property('barcode',th.StringType),
                th.Property('compareAtPrice',th.StringType),
                th.Property('createdAt',th.DateTimeType),
                th.Property('defaultCursor',th.StringType),
                th.Property('displayName',th.StringType),
                # th.Property('fulfilmentServiceEditable',th.ObjectType(
                #         th.Property('locked',th.BooleanType),
                #         th.Property('reason',th.StringType),
                #     )
                # ),
                th.Property('inventoryPolicy',th.StringType),
                th.Property('image',
                    th.ObjectType(
                    th.Property("id", th.StringType), th.Property("altText", th.StringType)
                    ),
                ),
                th.Property('inventoryQuantity',th.IntegerType),
                th.Property('legacyResourceId',th.StringType),
                th.Property('position',th.IntegerType),
                th.Property('price',th.StringType),
                # th.Property('price',th.ObjectType(
                #         th.Property('id',th.StringType)
                #     )
                # ),
                th.Property(
                    "selectedOptions",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("name", th.StringType),
                            th.Property("value", th.StringType),
                        )
                    ),
                ),
                th.Property('sku',th.StringType),
                th.Property('taxCode',th.StringType),
                th.Property('taxable',th.BooleanType),
                th.Property('title',th.StringType),
                th.Property('updatedAt',th.DateTimeType),
                th.Property('weight',th.NumberType),
                th.Property('weightUnit',th.StringType),
            )
        )
    ).to_dict()
