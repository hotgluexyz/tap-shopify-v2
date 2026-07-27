from hotglue_smoke_test.vcr.tap import VCRTapTestRunner

class ShopifyBetaTestRunner(VCRTapTestRunner):
    FILTER_HEADERS = [*VCRTapTestRunner.FILTER_HEADERS, "X-Shopify-Access-Token"]
    # Preserve only fields the tap reads from a response
    # and feeds into state or the next request.
    # I.E., replication_key, PK, pagination token.
    PRESERVE_KEYS = {
        "updatedAt",
        "issuedAt",
        "id",
        "cursor",
        "hasNextPage",
    }
    # What is not on the PRESERVE_KEYS will be heavily scrubbed.

    def module(self) -> str:
        return "tap_shopify_beta"

    def launch(self):
        from tap_shopify_beta.tap import TapshopifyBeta
        TapshopifyBeta.cli()


if __name__ == "__main__":
    ShopifyBetaTestRunner.main()
