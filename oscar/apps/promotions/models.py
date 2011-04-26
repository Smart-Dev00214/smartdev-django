"""
Vanilla promotion models
"""
from oscar.apps.promotions.abstract_models import (AbstractPromotion, AbstractPagePromotion, AbstractKeywordPromotion,
                                              BANNER, LEFT_POD, RIGHT_POD, RAW_HTML)


class Promotion(AbstractPromotion):
    pass


class PagePromotion(AbstractPagePromotion):
    pass


class KeywordPromotion(AbstractKeywordPromotion):
    pass