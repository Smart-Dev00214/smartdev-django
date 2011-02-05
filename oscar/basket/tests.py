from django.utils import unittest
from django.test.client import Client
from django.core.urlresolvers import reverse

from oscar.basket.models import * 
from oscar.product.models import Item, ItemClass


class BasketModelTest(unittest.TestCase):
    
    def setUp(self):
        self.basket = Basket.objects.create()
        
        # Create a dummy product
        ic,_ = ItemClass.objects.get_or_create(name='Dummy class')
        self.dummy_product = Item.objects.create(title='Dummy product', item_class=ic)
    
    def test_empty_baskets_have_zero_lines(self):
        self.assertTrue(Basket().num_lines == 0)
        
    def test_new_baskets_are_empty(self):
        self.assertTrue(Basket().is_empty)
        
    def test_basket_have_with_one_line(self):
        line = Line.objects.create(basket=self.basket, product=self.dummy_product)
        self.assertTrue(self.basket.num_lines == 1)
        
    def test_add_product_creates_line(self):
        self.basket.add_product(self.dummy_product)
        self.assertTrue(self.basket.num_lines == 1)
        
    def test_adding_multiproduct_line_returns_correct_number_of_items(self):
        self.basket.add_product(self.dummy_product, 10)
        self.assertEqual(self.basket.num_items, 10)
       
        
class BasketViewsTest(unittest.TestCase):
    
    def setUp(self):
        self.client = Client()
    
    def test_empty_basket_view(self):
        url = reverse('oscar-basket')
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(0, response.context['basket'].num_lines)
        
    def test_anonymous_add_to_basket_creates_cookie(self):
        ic,_ = ItemClass.objects.get_or_create(name='Dummy class')
        dummy_product = Item.objects.create(title='Dummy product', item_class=ic)
        url = reverse('oscar-basket')
        post_params = {'product_id': dummy_product.id,
                       'action': 'add',
                       'quantity': 1}
        response = self.client.post(url, post_params)
        self.assertTrue('oscar_open_basket' in response.cookies)
