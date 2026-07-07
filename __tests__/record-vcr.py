import os
import vcr
from hotglue_smoke_test.vcr.tap import VCRTapTestRunner

class ShopifyBetaTestRunner(VCRTapTestRunner):
    def __init__(self, test_case: str):
        super().__init__(test_case, os.path.dirname(os.path.abspath(__file__)))

    def module(self) -> str:
        return "tap_shopify_beta"

    def launch(self):
        from tap_shopify_beta.tap import TapshopifyBeta
        TapshopifyBeta.cli()

    def vcr_use_cassette(self, filter_query_parameters, test_config=None):
        return vcr.use_cassette(
            self.vcr_cassette_path,
            decode_compressed_response=True,
            filter_headers=["authorization", "X-Shopify-Access-Token"],
            filter_post_data_parameters=[
                "client_id",
                "client_secret",
                "refresh_token",
                "access_token",
            ],
            filter_query_parameters=filter_query_parameters,
            before_record_response=self.scrub_token_from_response,
        )

if __name__ == "__main__":
    ShopifyBetaTestRunner.main()
