from itertools import chain
import logging

from django.db.models import get_model

from oscar.apps.offer import results

ConditionalOffer = get_model('offer', 'ConditionalOffer')

logger = logging.getLogger('oscar.offers')


class OfferApplicationError(Exception):
    pass


class Applicator(object):

    def apply(self, request, basket):
        """
        Apply all relevant offers to the given basket.

        The request is passed too as sometimes the available offers
        are dependent on the user (eg session-based offers).
        """
        # Flush any existing discounts to make sure they are recalculated
        # correctly
        basket.reset_offer_applications()
        offers = self.get_offers(request, basket)
        self.apply_offers(basket, offers)

    def apply_offers(self, basket, offers):
        applications = results.OfferApplications()
        for offer in offers:
            num_applications = 0
            # Keep applying the offer until either
            # (a) We reach the max number of applications for the offer.
            # (b) The benefit can't be applied successfully.
            while num_applications < offer.get_max_applications(basket.owner):
                result = offer.apply_benefit(basket)
                num_applications += 1
                if not result.is_successful:
                    break
                applications.add(offer, result)
                if result.is_final:
                    break

        # Store this list of discounts with the basket so it can be
        # rendered in templates
        basket.offer_applications = applications

    def get_offers(self, request, basket):
        """
        Return all offers to apply to the basket.

        This method should be subclassed and extended to provide more
        sophisticated behaviour.  For instance, you could load extra offers
        based on the session or the user type.
        """
        site_offers = self.get_site_offers()
        basket_offers = self.get_basket_offers(basket, request.user)
        user_offers = self.get_user_offers(request.user)
        session_offers = self.get_session_offers(request)

        return list(chain(
            session_offers, basket_offers, user_offers, site_offers))

    def get_site_offers(self):
        """
        Return site offers that are available to all users
        """
        date_based_offers = ConditionalOffer.active.filter(
            offer_type=ConditionalOffer.SITE,
            status=ConditionalOffer.OPEN)
        nondate_based_offers = ConditionalOffer.objects.filter(
            offer_type=ConditionalOffer.SITE,
            status=ConditionalOffer.OPEN,
            start_datetime=None, end_datetime=None)
        return list(chain(date_based_offers, nondate_based_offers))

    def get_basket_offers(self, basket, user):
        """
        Return basket-linked offers such as those associated with a voucher
        code
        """
        offers = []
        if not basket.id:
            return offers

        for voucher in basket.vouchers.all():
            if voucher.is_active() and voucher.is_available_to_user(user):
                basket_offers = voucher.offers.all()
                for offer in basket_offers:
                    offer.set_voucher(voucher)
                offers = list(chain(offers, basket_offers))
        return offers

    def get_user_offers(self, user):
        """
        Returns offers linked to this particular user.

        Eg: student users might get 25% off
        """
        return []

    def get_session_offers(self, request):
        """
        Returns temporary offers linked to the current session.

        Eg: visitors coming from an affiliate site get a 10% discount
        """
        return []
