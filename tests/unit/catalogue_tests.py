from django.test import TestCase
from django.core.exceptions import ValidationError

from oscar.apps.catalogue.models import Product, ProductClass, Category, \
        ProductAttribute
from oscar.apps.catalogue.categories import create_from_breadcrumbs


class TestProductClassModel(TestCase):

    def test_slug_is_auto_created(self):
        books = ProductClass.objects.create(
            name="Book",
        )
        self.assertEqual('book', books.slug)

    def test_has_attribute_for_whether_shipping_is_required(self):
        ""
        ProductClass.objects.create(
            name="Download",
            requires_shipping=False
        )


class TestCategoryFactory(TestCase):

    def setUp(self):
        Category.objects.all().delete()
    
    def test_can_create_single_level_category(self):
        trail = 'Books'
        category = create_from_breadcrumbs(trail)
        self.assertIsNotNone(category)
        self.assertEquals(category.name, 'Books')
        self.assertEquals(category.slug, 'books')      
    
    def test_can_create_parent_and_child_categories(self):
        trail = 'Books > Science-Fiction'
        category = create_from_breadcrumbs(trail)
        
        self.assertIsNotNone(category)
        self.assertEquals(category.name, 'Science-Fiction')
        self.assertEquals(category.get_depth(), 2)
        self.assertEquals(category.get_parent().name, 'Books')
        self.assertEquals(2, Category.objects.count())
        self.assertEquals(category.slug, 'books/science-fiction')
        
    def test_can_create_multiple_categories(self):
        trail = 'Books > Science-Fiction > Star Trek'
        create_from_breadcrumbs(trail)
        trail = 'Books > Factual > Popular Science'
        category = create_from_breadcrumbs(trail)
        
        self.assertIsNotNone(category)
        self.assertEquals(category.name, 'Popular Science')
        self.assertEquals(category.get_depth(), 3)
        self.assertEquals(category.get_parent().name, 'Factual')
        self.assertEquals(5, Category.objects.count())
        self.assertEquals(category.slug, 'books/factual/popular-science', )        

    def test_can_use_alternative_separator(self):
        trail = 'Food|Cheese|Blue'
        create_from_breadcrumbs(trail, separator='|')
        self.assertEquals(3, len(Category.objects.all()))


class ProductTests(TestCase):

    def setUp(self):
        self.product_class,_ = ProductClass.objects.get_or_create(name='Clothing')


class ProductCreationTests(ProductTests):

    def setUp(self):
        super(ProductCreationTests, self).setUp()
        ProductAttribute.objects.create(product_class=self.product_class,
                                        name='Number of pages',
                                        code='num_pages',
                                        type='integer')
        Product.ENABLE_ATTRIBUTE_BINDING = True

    def tearDown(self):
        Product.ENABLE_ATTRIBUTE_BINDING = False

    def test_create_products_with_attributes(self):
        product = Product(upc='1234',
                          product_class=self.product_class,
                          title='testing')
        product.attr.num_pages = 100
        product.save()
   

class TopLevelProductTests(ProductTests):
    
    def test_top_level_products_must_have_titles(self):
        self.assertRaises(ValidationError, Product.objects.create, product_class=self.product_class)
        
        
class VariantProductTests(ProductTests):
    
    def setUp(self):
        super(VariantProductTests, self).setUp()
        self.parent = Product.objects.create(title="Parent product", product_class=self.product_class)
    
    def test_variant_products_dont_need_titles(self):
        Product.objects.create(parent=self.parent, product_class=self.product_class)
        
    def test_variant_products_dont_need_a_product_class(self):
        Product.objects.create(parent=self.parent)
       
    def test_variant_products_inherit_parent_titles(self):
        p = Product.objects.create(parent=self.parent, product_class=self.product_class)
        self.assertEquals("Parent product", p.get_title())
        
    def test_variant_products_inherit_product_class(self):
        p = Product.objects.create(parent=self.parent)
        self.assertEquals("Clothing", p.get_product_class().name)
