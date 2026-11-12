import json
from urllib.parse import urlsplit, urlunsplit

import vcr
from hotglue_smoke_test.vcr.tap import VCRTapTestRunner

class ShopifyBetaTestRunner(VCRTapTestRunner):
    FILTER_HEADERS = [
        *VCRTapTestRunner.FILTER_HEADERS,
        "X-Shopify-Access-Token",
        "nel", "report-to", "reporting-endpoints", "content-security-policy",
        "server-timing", "cf-ray", "shopify-edge-ip", "x-request-id", "x-dc",
        "x-shardid", "x-shopid", "x-sorting-hat-podid", "x-sorting-hat-shopid",
        "x-stats-apiclientid", "x-stats-apipermissionid", "x-stats-userid",
    ]
    TOKEN_KEYS = [*VCRTapTestRunner.TOKEN_KEYS, "redirect_uri"]
    # Preserve only fields the tap reads from a response
    # and feeds into state or the next request.
    # I.E., replication_key, PK, pagination token.
    PRESERVE_KEYS = {
        "updatedAt",
        "issuedAt",
        "id",
        "cursor",
        "hasNextPage",
        "count",
    }
    # What is not on the PRESERVE_KEYS will be heavily scrubbed.

    def scrub_uri(self, uri: str) -> str:
        parts = urlsplit(uri)
        if parts.hostname and parts.hostname.endswith(".myshopify.com"):
            return urlunsplit(parts._replace(netloc="fake-shop.myshopify.com"))
        return uri

    def vcr_use_cassette(self, filter_query_parameters):
        return vcr.use_cassette(
            self.vcr_cassette_path,
            record_mode="once" if self.mode == "record" else "none",
            decode_compressed_response=True,
            filter_headers=list(self.FILTER_HEADERS),
            filter_post_data_parameters=list(self.TOKEN_KEYS),
            filter_query_parameters=filter_query_parameters,
            before_record_response=self.before_record_response,
        )

    def scrub_response_body(self, body, faker, cache):
        original = json.loads(body)
        scrubbed = json.loads(super().scrub_response_body(body, faker, cache))
        # Query costs determine page size; error codes choose retry vs. failure.
        if "cost" in original.get("extensions", {}):
            scrubbed["extensions"]["cost"] = original["extensions"]["cost"]
        for error, fake_error in zip(original.get("errors", []), scrubbed.get("errors", [])):
            if "code" in error.get("extensions", {}):
                fake_error["extensions"]["code"] = error["extensions"]["code"]
        return json.dumps(scrubbed)

    def module(self) -> str:
        return "tap_shopify_beta"

    def launch(self):
        from tap_shopify_beta.tap import TapshopifyBeta
        TapshopifyBeta.cli()


if __name__ == "__main__":
    ShopifyBetaTestRunner.main()
