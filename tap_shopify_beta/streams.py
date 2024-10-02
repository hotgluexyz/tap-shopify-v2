"""Stream type classes for tap-shopify-beta."""
import abc
import json
from typing import Optional

from singer_sdk import typing as th

from tap_shopify_beta.client_bulk import shopifyBulkStream
from tap_shopify_beta.client_gql import shopifyGqlStream
from tap_shopify_beta.client_rest import shopifyRestStream
from tap_shopify_beta.types.customer_visit import CustomerVisitType

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
with open("config.json", "r") as jsonfile:
    data = json.load(jsonfile)

stream_condition = data.get("bulk", True)
class DynamicStream(shopifyBulkStream if stream_condition else shopifyGqlStream):
    pass

class ProductsStream(DynamicStream):
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


class VariantsStream(DynamicStream):
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


class OrdersStream(DynamicStream):
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
            "disputes",th.ArrayType(
            th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("initiatedAs", th.StringType),
                th.Property("status", th.StringType),
            ))
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
                        "trackingInfo",th.ArrayType(
                        th.ObjectType(
                            th.Property("company", th.StringType),
                            th.Property("number", th.StringType),
                            th.Property("url", th.StringType),
                        ))
                    ),
                    th.Property("updatedAt", th.DateTimeType),
                )
            ),
        ),
        th.Property("fullyPaid", th.BooleanType),
        th.Property("legacyResourceId", th.StringType),
        th.Property("hasTimelineComment", th.BooleanType),
        th.Property("merchantEditable", th.BooleanType),
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
            th.ArrayType(th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("createdAt", th.DateTimeType),
                th.Property(
                    "duties",
                    th.ArrayType(th.ObjectType(
                        th.Property("amountSet", MoneyBag),
                    )),
                ),
                th.Property("legacyResourceId", th.StringType),
                th.Property("note", th.StringType),
                th.Property("totalRefundedSet", MoneyBag),
                th.Property("updatedAt", th.DateTimeType),
            ),
        )),
        th.Property("registeredSourceUrl", th.StringType),
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
                th.Property("custom", th.BooleanType),
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
        th.Property("sourceIdentifier", th.StringType),
    ).to_dict()


class ShopStream(shopifyGqlStream):
    """Define shop stream."""

    name = "shop"
    primary_keys = ["id"]
    query_name = "shop"
    replication_key = None
    is_list = False

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


class InventoryItemsStream(DynamicStream):
    """Define Intentory Items stream."""

    name = "inventory_items"
    primary_keys = ["id"]
    query_name = "inventoryItems"
    replication_key = "updatedAt"

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("countryCodeOfOrigin", th.StringType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("duplicateSkuCount", th.IntegerType),
        th.Property("harmonizedSystemCode", th.StringType),
        th.Property("inventoryHistoryUrl", th.StringType),
        th.Property("legacyResourceId", th.StringType),
        th.Property("locationsCount", th.IntegerType),
        th.Property("provinceCodeOfOrigin", th.StringType),
        th.Property("requiresShipping", th.BooleanType),
        th.Property("sku", th.StringType),
        th.Property("tracked", th.BooleanType),
        th.Property(
            "trackedEditable",
            th.ObjectType(
                th.Property("locked", th.BooleanType),
                th.Property("reason", th.StringType),
            ),
        ),
        th.Property(
            "unitCost",
            th.ObjectType(
                th.Property("amount", th.StringType),
                th.Property("currencyCode", th.StringType),
            ),
        ),
        th.Property("updatedAt", th.DateTimeType),
        th.Property(
            "variant",
            th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("availableForSale", th.BooleanType),
                th.Property("barcode", th.StringType),
                th.Property("compareAtPrice", th.StringType),
                th.Property("createdAt", th.DateTimeType),
                th.Property("defaultCursor", th.StringType),
                th.Property("displayName", th.StringType),
                # th.Property('fulfilmentServiceEditable',th.ObjectType(
                #         th.Property('locked',th.BooleanType),
                #         th.Property('reason',th.StringType),
                #     )
                # ),
                th.Property("inventoryPolicy", th.StringType),
                th.Property(
                    "image",
                    th.ObjectType(
                        th.Property("id", th.StringType),
                        th.Property("altText", th.StringType),
                    ),
                ),
                th.Property("inventoryQuantity", th.IntegerType),
                th.Property("legacyResourceId", th.StringType),
                th.Property("position", th.IntegerType),
                th.Property("price", th.StringType),
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
                th.Property("sku", th.StringType),
                th.Property("taxCode", th.StringType),
                th.Property("taxable", th.BooleanType),
                th.Property("title", th.StringType),
                th.Property("updatedAt", th.DateTimeType),
                th.Property("weight", th.NumberType),
                th.Property("weightUnit", th.StringType),
            ),
        ),
    ).to_dict()


class CollectionsStream(DynamicStream):
    """Define collections stream."""

    name = "collections"
    primary_keys = ["id"]
    query_name = "collections"
    replication_key = "updatedAt"

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("description", th.StringType),
        th.Property("descriptionHtml", th.StringType),
        th.Property("handle", th.StringType),
        th.Property(
            "image",
            th.ObjectType(
                th.Property("id", th.StringType), th.Property("altText", th.StringType)
            ),
        ),
        th.Property("legacyResourceId", th.StringType),
        th.Property("productsCount", th.IntegerType),
        th.Property("sortOrder", th.StringType),
        th.Property("templateSuffix", th.StringType),
        th.Property("title", th.StringType),
        th.Property("updatedAt", th.DateTimeType),
    ).to_dict()


class CustomersStream(DynamicStream):
    """Define collections stream."""

    name = "customers"
    primary_keys = ["id"]
    query_name = "customers"
    replication_key = "updatedAt"
    sort_key = "UPDATED_AT"
    sort_key_type = "CustomerSortKeys"

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("id", th.StringType),
        th.Property("firstName", th.StringType),
        th.Property("lastName", th.StringType),
        th.Property("email", th.StringType),
        th.Property("phone", th.StringType),
        th.Property("numberOfOrders", th.StringType),
        th.Property(
            "amountSpent",
            th.ObjectType(
                th.Property("amount", th.StringType),
                th.Property("currencyCode", th.StringType),
            ),
        ),
        th.Property("note", th.StringType),
        th.Property("verifiedEmail", th.BooleanType),
        th.Property("validEmailAddress", th.BooleanType),
        th.Property("tags", th.CustomType({"type": ["array", "string"]})),
        th.Property("lifetimeDuration", th.StringType),
        th.Property(
            "defaultAddress",
            th.ObjectType(
                th.Property("address1", th.StringType),
                th.Property("address2", th.StringType),
                th.Property("city", th.StringType),
                th.Property("company", th.StringType),
                th.Property("country", th.StringType),
                th.Property("countryCodeV2", th.StringType),
                th.Property("firstName", th.StringType),
                th.Property("formatted", th.CustomType({"type": ["array", "string"]})),
                th.Property("formattedArea", th.StringType),
                th.Property("id", th.StringType),
                th.Property("lastName", th.StringType),
                th.Property("name", th.StringType),
                th.Property("phone", th.StringType),
                th.Property("province", th.StringType),
                th.Property("provinceCode", th.StringType),
                th.Property("zip", th.StringType),
                th.Property("latitude", th.NumberType),
                th.Property("longitude", th.NumberType),
            ),
        ),
        th.Property(
            "addresses",
            th.ArrayType(
                th.ObjectType(
                    th.Property("address1", th.StringType),
                    th.Property("address2", th.StringType),
                    th.Property("city", th.StringType),
                    th.Property("company", th.StringType),
                    th.Property("country", th.StringType),
                    th.Property("countryCodeV2", th.StringType),
                    th.Property("firstName", th.StringType),
                    th.Property("formatted", th.CustomType({"type": ["array", "string"]})),
                    th.Property("formattedArea", th.StringType),
                    th.Property("id", th.StringType),
                    th.Property("lastName", th.StringType),
                    th.Property("name", th.StringType),
                    th.Property("phone", th.StringType),
                    th.Property("province", th.StringType),
                    th.Property("provinceCode", th.StringType),
                    th.Property("zip", th.StringType),
                    th.Property("latitude", th.NumberType),
                    th.Property("longitude", th.NumberType),
                )
            ),
        ),
        th.Property(
            "image",
            th.ObjectType(
                th.Property("src", th.StringType),
                th.Property("width", th.NumberType),
                th.Property("height", th.NumberType),
                th.Property("altText", th.StringType),
            ),
        ),
        th.Property("canDelete", th.BooleanType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property("emailMarketingConsent", th.ObjectType(
            th.Property("consentUpdatedAt", th.DateTimeType),
            th.Property("marketingOptInLevel", th.StringType),
            th.Property("marketingState", th.StringType),
        )),
        th.Property("smsMarketingConsent", th.ObjectType(
            th.Property("consentCollectedFrom", th.StringType),
            th.Property("consentUpdatedAt", th.DateTimeType),
            th.Property("marketingOptInLevel", th.StringType),
            th.Property("marketingState", th.StringType),
        )),
    ).to_dict()


class LocationsStream(shopifyRestStream):
    """Define collections stream."""

    path = "locations.json"
    name = "locations"
    primary_keys = ["id"]
    replication_key = None
    records_jsonpath = "$.locations.[*]"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("address1", th.StringType),
        th.Property("address2", th.StringType),
        th.Property("city", th.StringType),
        th.Property("zip", th.StringType),
        th.Property("province", th.StringType),
        th.Property("country", th.StringType),
        th.Property("phone", th.StringType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("country_code", th.StringType),
        th.Property("country_name", th.StringType),
        th.Property("province_code", th.StringType),
        th.Property("legacy", th.BooleanType),
        th.Property("active", th.BooleanType),
        th.Property("admin_graphql_api_id", th.StringType),
        th.Property("localized_country_name", th.StringType),
        th.Property("localized_province_name", th.StringType),
    ).to_dict()

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "location_id": record["id"],
        }


class InventoryLevelRestStream(shopifyRestStream):
    """Define collections stream."""

    path = "inventory_levels.json"
    name = "inventory_level_rest"
    primary_keys = ["id"]
    records_jsonpath = "$.inventory_levels.[*]"

    @property
    def add_params(self):
        location_id = self.tap_state.get("bookmarks").get("inventory_level_rest").get("partitions")[-1]["context"]["location_id"]
        params = {"location_ids": location_id}
        if self.config.get("inventory_item_ids"):
            item_ids = self.config.get("inventory_item_ids")
            if isinstance(item_ids,list):
                item_ids = ",".join(item_ids)
            params.update({"inventory_item_ids":item_ids})
        return params

    parent_stream_type = LocationsStream

    schema = th.PropertiesList(
        th.Property("admin_graphql_api_id", th.StringType),
    ).to_dict()

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "inventory_level_id": record["admin_graphql_api_id"],
        }


class InventoryLevelGqlStream(shopifyGqlStream):
    """Define collections stream."""

    name = "inventory_level_gql"
    primary_keys = ["id"]
    replication_key = None
    parent_stream_type = InventoryLevelRestStream
    query_name = "inventoryLevel"
    is_list = False

    @property
    def single_object_params(self):
        inventory_level_id = self.tap_state.get("bookmarks").get("inventory_level_gql").get("partitions")[0]["context"]["inventory_level_id"]
        return {"id": inventory_level_id}

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("available", th.IntegerType),
        th.Property("incoming", th.IntegerType),
        th.Property("item", th.ObjectType(
            th.Property("id", th.StringType),
            th.Property("sku", th.StringType),
        )),
        th.Property("location", th.ObjectType(
            th.Property("id", th.StringType),
            th.Property("name", th.StringType),
        )),
    ).to_dict()


class PriceRulesStream(shopifyRestStream):
    """Define collections stream."""

    name = "price_rules"
    primary_keys = ["id"]
    replication_key = "updated_at"
    records_jsonpath = "$.price_rules.[*]"
    path = "price_rules.json"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("value_type", th.StringType),
        th.Property("value", th.StringType),
        th.Property("customer_selection", th.StringType),
        th.Property("target_type", th.StringType),
        th.Property("target_selection", th.StringType),
        th.Property("allocation_method", th.StringType),
        th.Property("allocation_limit", th.StringType),
        th.Property("once_per_customer", th.BooleanType),
        th.Property("usage_limit", th.IntegerType),
        th.Property("starts_at", th.DateTimeType),
        th.Property("ends_at", th.DateTimeType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("entitled_product_ids", th.ArrayType(th.IntegerType)),
        th.Property("entitled_variant_ids", th.ArrayType(th.IntegerType)),
        th.Property("entitled_collection_ids", th.ArrayType(th.IntegerType)),
        th.Property("entitled_country_ids", th.ArrayType(th.IntegerType)),
        th.Property("prerequisite_product_ids", th.ArrayType(th.IntegerType)),
        th.Property("prerequisite_variant_ids", th.ArrayType(th.IntegerType)),
        th.Property("prerequisite_collection_ids", th.ArrayType(th.IntegerType)),
        th.Property("prerequisite_saved_search_ids", th.ArrayType(th.IntegerType)),
        th.Property("customer_segment_prerequisite_ids", th.ArrayType(th.IntegerType)),
        th.Property("prerequisite_customer_ids", th.ArrayType(th.IntegerType)),
        th.Property("prerequisite_subtotal_range", th.StringType),
        th.Property("prerequisite_quantity_range", th.ObjectType(
            th.Property("greater_than_or_equal_to", th.IntegerType)
        )),
        th.Property("prerequisite_shipping_price_range", th.ObjectType(
            th.Property("less_than_or_equal_to", th.IntegerType)
        )),
        th.Property("prerequisite_to_entitlement_quantity_ratio", th.ObjectType(
            th.Property("prerequisite_quantity", th.StringType),
            th.Property("entitled_quantity", th.IntegerType),
        )),
        th.Property("prerequisite_to_entitlement_purchase", th.ObjectType(					
            th.Property("prerequisite_amount", th.StringType),
        )),
        th.Property("prerequisite_subtotal_range", th.ObjectType(					
            th.Property("greater_than_or_equal_to", th.StringType),
        )),
        th.Property("title", th.StringType),
        th.Property("_sdc_shop_myshopify_domain", th.StringType),
        th.Property("_sdc_shop_id", th.IntegerType),
        th.Property("_sdc_shop_name", th.StringType),
        th.Property("admin_graphql_api_id", th.StringType),
    ).to_dict()


class EventProductsStream(shopifyRestStream):
    """Define collections stream."""

    name = "event_products"
    primary_keys = ["id"]
    replication_key = "created_at"
    records_jsonpath = "$.events.[*]"
    path = "events.json"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("subject_id", th.IntegerType),
        th.Property("created_at", th.DateTimeType),
        th.Property("subject_type", th.StringType),
        th.Property("verb", th.StringType),
        th.Property("arguments", th.ArrayType(th.CustomType({"type": ["number", "string", "null", "object"]}))),
        th.Property("body", th.StringType),
        th.Property("message", th.StringType),
        th.Property("author", th.StringType),
        th.Property("description", th.StringType),
        th.Property("path", th.StringType),
    ).to_dict()


class MarketingEventsStream(shopifyRestStream):
    """Define collections stream."""

    name = "marketing_events"
    primary_keys = ["id"]
    path = "marketing_events.json"
    records_jsonpath= "$.marketing_events.[*]"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("event_type", th.StringType),
        th.Property("remote_id", th.StringType),
        th.Property("started_at", th.DateTimeType),
        th.Property("ended_at", th.DateTimeType),
        th.Property("scheduled_to_end_at", th.DateTimeType),
        th.Property("budget", th.NumberType),
        th.Property("currency", th.StringType),
        th.Property("manage_url", th.StringType),
        th.Property("preview_url", th.StringType),
        th.Property("utm_campaign", th.StringType),
        th.Property("utm_source", th.StringType),
        th.Property("utm_medium", th.StringType),
        th.Property("budget_type", th.StringType),
        th.Property("description", th.StringType),
        th.Property("marketing_channel", th.StringType),
        th.Property("paid", th.BooleanType),
        th.Property("referring_domain", th.StringType),
        th.Property("breadcrumb_id", th.IntegerType),
        th.Property("marketing_activity_id", th.IntegerType),
        th.Property("admin_graphql_api_id", th.StringType),
        th.Property("marketed_resources", th.ArrayType(
            th.ObjectType(
                th.Property("type", th.StringType),
                th.Property("id", th.IntegerType), 
            )
        )),
    ).to_dict()


class EventDestroyedProductsStream(EventProductsStream):
    """Define collections stream."""

    name = "event_destroyed_products"
    add_params = {"verb": "destroy"}


class CustomerVisitStream(shopifyGqlStream, metaclass=abc.ABCMeta):
    """Define base class for CustomerVisit stream"""

    primary_keys = ["id", "updatedAt"]
    query_name = "orders"
    replication_key = "updatedAt"
    page_size = 100
    is_timestamp_replication_key = True
    json_path = "$.edges[*].node"  # JSONPath to compile over the result of filter_response()

    @property
    def schema(self):
        return th.PropertiesList(
            th.Property("id", th.StringType),
            th.Property("updatedAt", th.DateTimeType),
            th.Property("customerJourneySummary", th.ObjectType(
                th.Property(self.visit_type, CustomerVisitType())
            ))
        ).to_dict()
    
    def filter_response(self, response_json: dict) -> dict:
        return {
            'edges': [
                e
                for e in response_json['data']['orders']['edges'] 
                if e.get('node',{}).get('customerJourneySummary',{}).get(self.visit_type)
            ]
        }

class CustomerFirstVisitStream(CustomerVisitStream):
    """Define Customer Visit stream"""

    name = "customer_first_visit"
    
    @property
    def visit_type(self) -> str:
        return "firstVisit"

class CustomerLastVisitsStream(CustomerVisitStream):
    """Define Customer Visit stream"""

    name = "customer_last_visit"
    
    @property
    def visit_type(self) -> str:
        return "lastVisit"


class CustomerJourneySummaryStream(shopifyGqlStream):
    """Define base class for CustomerVisit stream"""

    name = "customer_journey_summary"
    primary_keys = ["id", "updatedAt"]
    query_name = "orders"
    replication_key = "updatedAt"
    page_size = 100
    is_timestamp_replication_key = True

    schema = th.PropertiesList(
            th.Property("id", th.StringType),
            th.Property("updatedAt", th.DateTimeType),
            th.Property("customerJourneySummary", th.ObjectType(
                th.Property("customerOrderIndex", th.IntegerType),
                th.Property("daysToConversion", th.IntegerType),
                th.Property("firstVisit", CustomerVisitType()),
                th.Property("lastVisit", CustomerVisitType()),
                th.Property("momentsCount", th.IntegerType),
                th.Property("ready", th.BooleanType),
            ))
    ).to_dict()