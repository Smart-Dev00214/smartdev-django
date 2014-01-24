from django.test import TestCase

from oscar.apps.partner import availability


class TestBasePolicy(TestCase):

    def setUp(self):
        self.availability = availability.Base()

    def test_does_not_allow_any_purchases(self):
        result, __ = self.availability.is_purchase_permitted(1)
        self.assertFalse(result)

    def test_is_not_available_to_buy(self):
        result = self.availability.is_available_to_buy
        self.assertFalse(result)


class TestUnavailablePolicy(TestCase):

    def setUp(self):
        self.availability = availability.Unavailable()

    def test_is_unavailable(self):
        self.assertFalse(self.availability.is_available_to_buy)

    def test_does_not_allow_any_purchases(self):
        result, __ = self.availability.is_purchase_permitted(1)
        self.assertFalse(result)

    def test_gives_a_reason_for_unavailability(self):
        __, msg = self.availability.is_purchase_permitted(1)
        self.assertEqual("Unavailable", msg)

    def test_returns_availability_code(self):
        self.assertEqual('unavailable', self.availability.code)


class TestStockRequiredWrapperForRecordWithStock(TestCase):

    def setUp(self):
        self.availability = availability.StockRequired(5)

    def test_is_available_to_buy(self):
        self.assertTrue(self.availability.is_available_to_buy)

    def test_permits_purchases_up_to_stock_level(self):
        for x in range(0, 6):
            is_permitted, __ = self.availability.is_purchase_permitted(x)
            self.assertTrue(is_permitted)

    def test_forbids_purchases_over_stock_level(self):
        is_permitted, __ = self.availability.is_purchase_permitted(7)
        self.assertFalse(is_permitted)

    def test_returns_correct_code(self):
        self.assertEqual('instock', self.availability.code)

    def test_returns_correct_message(self):
        self.assertEqual('In stock (5 available)', self.availability.message)


class TestStockRequiredWrapperForRecordWithoutStock(TestCase):

    def setUp(self):
        self.availability = availability.StockRequired(0)

    def test_is_available_to_buy(self):
        self.assertFalse(self.availability.is_available_to_buy)

    def test_forbids_purchases(self):
        is_permitted, __ = self.availability.is_purchase_permitted(1)
        self.assertFalse(is_permitted)

    def test_returns_correct_code(self):
        self.assertEqual('outofstock', self.availability.code)

    def test_returns_correct_message(self):
        self.assertEqual('Unavailable', self.availability.message)


class TestAvailableWrapper(TestCase):

    def setUp(self):
        self.availability = availability.Available()

    def test_is_available_to_buy(self):
        self.assertTrue(self.availability.is_available_to_buy)

    def test_permits_any_purchase(self):
        is_permitted, __ = self.availability.is_purchase_permitted(10000)
        self.assertTrue(is_permitted)

    def test_returns_correct_code(self):
        self.assertEqual('available', self.availability.code)

    def test_returns_correct_message(self):
        self.assertEqual('Available', self.availability.message)
