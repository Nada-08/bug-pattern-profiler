from packages.retrieval.models import QueryEntities
from packages.retrieval.query_normalizer import QueryNormalizer
from packages.retrieval.extractors.regex_extractor import RegexExtractor
from packages.retrieval.extractors.date_extractor import DateExtractor
from packages.retrieval.utils.candidate_generator import CandidateGenerator
from packages.retrieval.extractors.vendor_product_extractor import VendorProductResolver

class QueryParser:

    def __init__(self):
        self.normalizer = QueryNormalizer()
        self.regex = RegexExtractor()
        self.date_extractor = DateExtractor()
        self.candidate_generator = CandidateGenerator()
        self.vendor_product_resolver = VendorProductResolver()

    def parse(self, query: str) -> QueryEntities:
        normalized_query = self.normalizer.normalize(query)

        candidates = self.candidate_generator.generate(normalized_query)

        vendor_product = self.vendor_product_resolver.extract(candidates)


        entities = {
            **self.regex.extract(normalized_query),
            **self.date_extractor.extract(normalized_query),

            "vendor": vendor_product.vendor,
            "vendor_confidence": vendor_product.vendor_confidence,
            "product": vendor_product.product,
            "product_confidence": vendor_product.product_confidence,
        }
        
        return QueryEntities(**entities)
    