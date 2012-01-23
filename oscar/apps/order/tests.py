from decimal import Decimal as D
import hashlib

from django.test import TestCase
from django.conf import settings
from mock import Mock

from oscar.apps.address.models import Country
from oscar.apps.basket.models import Basket
from oscar.apps.order.models import ShippingAddress, Order, Line, ShippingEvent, ShippingEventType, ShippingEventQuantity
from oscar.test.helpers import create_order, create_product
from oscar.apps.order.utils import OrderCreator
from oscar.apps.shipping.methods import Free

ORDER_PLACED = 'order_placed'


class ShippingAddressTest(TestCase):
    
    def test_titleless_salutation_is_stripped(self):
        country = Country.objects.get(iso_3166_1_a2='GB')
        a = ShippingAddress.objects.create(last_name='Barrington', line1="75 Smith Road", postcode="N4 8TY", country=country)
        self.assertEquals("Barrington", a.salutation())
    

class OrderTest(TestCase):
    fixtures = ['sample-order.json']

    def setUp(self):
        self.order = Order.objects.get(number='100002')
        
    def event(self, type):
        """
        Creates an order-level shipping event
        """
        type = ShippingEventType.objects.get(code=type)
        event = ShippingEvent.objects.create(order=self.order, event_type=type)
        for line in self.order.lines.all():
            ShippingEventQuantity.objects.create(event=event, line=line)  
        
    def test_shipping_status_is_empty_with_no_events(self):
        self.assertEquals("", self.order.shipping_status)

    def test_shipping_status_after_one_order_level_events(self):
        self.event(ORDER_PLACED)
        self.assertEquals("Order placed", self.order.shipping_status)

    def test_order_hash_generation(self):
        order = create_order()
        expected = hashlib.md5("%s%s" % (order.number, settings.SECRET_KEY)).hexdigest()
        self.assertEqual(expected, order.verification_hash())

        
class LineTest(TestCase):
    fixtures = ['sample-order.json']

    def setUp(self):
        self.order = Order.objects.get(number='100002')
        self.line = self.order.lines.get(id=1)

    def event(self, type, quantity=None):
        """
        Creates a shipping event for the test line
        """
        event = ShippingEvent.objects.create(order=self.order, event_type=type)
        if quantity == None:
            quantity = self.line.quantity
        event_quantity = ShippingEventQuantity.objects.create(event=event, line=self.line, quantity=quantity)

    def test_shipping_status_is_empty_to_start_with(self):
        self.assertEquals('', self.line.shipping_status)
        
    def test_shipping_status_after_full_line_event(self):
        type = ShippingEventType.objects.get(code='order_placed')
        self.event(type)
        self.assertEquals(type.name, self.line.shipping_status)    
        
    def test_shipping_status_after_two_full_line_events(self):
        type1 = ShippingEventType.objects.get(code='order_placed')
        self.event(type1)
        type2 = ShippingEventType.objects.get(code='dispatched')
        self.event(type2)
        self.assertEquals(type2.name, self.line.shipping_status) 
        
    def test_shipping_status_after_partial_line_event(self):
        type = ShippingEventType.objects.get(code='order_placed')
        self.event(type, 3)
        expected = "%s (%d/%d items)" % (type.name, 3, self.line.quantity)
        self.assertEquals(expected, self.line.shipping_status) 
        
    def test_has_passed_shipping_status_after_full_line_event(self):
        type = ShippingEventType.objects.get(code='order_placed')
        self.event(type)
        self.assertTrue(self.line.has_shipping_event_occurred(type)) 
        
    def test_has_passed_shipping_status_after_partial_line_event(self):
        type = ShippingEventType.objects.get(code='order_placed')
        self.event(type, self.line.quantity - 1)
        self.assertFalse(self.line.has_shipping_event_occurred(type)) 
        
    def test_has_passed_shipping_status_after_multiple_line_event(self):
        event_types = [ShippingEventType.objects.get(code='order_placed'),
                        ShippingEventType.objects.get(code='dispatched')]
        for type in event_types:
            self.event(type)
        for type in event_types:
            self.assertTrue(self.line.has_shipping_event_occurred(type))
            
    def test_inconsistent_shipping_status_setting(self):
        type = ShippingEventType.objects.get(code='order_placed')
        self.event(type, self.line.quantity - 1)
        
        with self.assertRaises(ValueError):
            # Quantity is higher for second event than first
            type = ShippingEventType.objects.get(code='dispatched')
            self.event(type, self.line.quantity)
        
    def test_inconsistent_shipping_quantities(self):
        type = ShippingEventType.objects.get(code='order_placed')
        self.event(type, self.line.quantity - 1)
        
        with self.assertRaises(ValueError):
            # Total quantity is too high
            self.event(type, 2)
        
        
class ShippingEventQuantityTest(TestCase):
    fixtures = ['sample-order.json']

    def setUp(self):
        self.order = Order.objects.get(number='100002')
        self.line = self.order.lines.get(id=1)

    def test_quantity_defaults_to_all(self):
        type = ShippingEventType.objects.get(code='order_placed')
        event = ShippingEvent.objects.create(order=self.order, event_type=type)
        event_quantity = ShippingEventQuantity.objects.create(event=event, line=self.line)
        self.assertEquals(self.line.quantity, event_quantity.quantity)
    
   
class OrderCreatorTests(TestCase):

    def setUp(self):
        self.creator = OrderCreator()
        self.basket = Basket.objects.create()

    def tearDown(self):
        Order.objects.all().delete()

    def test_exception_raised_when_empty_basket_passed(self):
        with self.assertRaises(ValueError):
            self.creator.place_order(basket=self.basket)

    def test_order_models_are_created(self):
        self.basket.add_product(create_product(price=D('12.00')))
        self.creator.place_order(basket=self.basket, order_number='1234')
        order = Order.objects.get(number='1234')
        lines = order.lines.all()
        self.assertEqual(1, len(lines))

    def test_status_is_saved_if_passed(self):
        self.basket.add_product(create_product(price=D('12.00')))
        self.creator.place_order(basket=self.basket, order_number='1234', status='Active')
        order = Order.objects.get(number='1234')
        self.assertEqual('Active', order.status)

    def test_shipping_is_free_by_default(self):
        self.basket.add_product(create_product(price=D('12.00')))
        self.creator.place_order(basket=self.basket, order_number='1234')
        order = Order.objects.get(number='1234')
        self.assertEqual(order.total_incl_tax, self.basket.total_incl_tax)
        self.assertEqual(order.total_excl_tax, self.basket.total_excl_tax)

    def test_basket_totals_are_used_by_default(self):
        self.basket.add_product(create_product(price=D('12.00')))
        method = Mock()
        method.basket_charge_incl_tax = Mock(return_value=D('2.00'))
        method.basket_charge_excl_tax = Mock(return_value=D('2.00'))

        self.creator.place_order(basket=self.basket, order_number='1234', shipping_method=method)
        order = Order.objects.get(number='1234')
        self.assertEqual(order.total_incl_tax, self.basket.total_incl_tax + D('2.00'))
        self.assertEqual(order.total_excl_tax, self.basket.total_excl_tax + D('2.00'))
        
    def test_exception_raised_if_duplicate_number_passed(self):
        self.basket.add_product(create_product(price=D('12.00')))
        self.creator.place_order(basket=self.basket, order_number='1234')
        with self.assertRaises(ValueError):
            self.creator.place_order(basket=self.basket, order_number='1234')

