"""
Models of products
"""
import re

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse


def _convert_to_underscores(str):
    """
    For converting a string in CamelCase or normal text with spaces
    to the normal underscored variety
    """
    without_whitespace = re.sub('\s*', '', str)
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', without_whitespace)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class AbstractItemClass(models.Model):
    """
    Defines an item type (equivqlent to Taoshop's MediaType).
    """
    name = models.CharField(_('name'), max_length=128)
    slug = models.SlugField(max_length=128)

    class Meta:
        abstract = True
        ordering = ['name']
        verbose_name_plural = "Item classes"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug= slugify(self.name)
        super(AbstractItemClass, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('oscar-product-item-class', kwargs={'item_class_slug': self.slug})

    def __unicode__(self):
        return self.name


class BrowsableItemManager(models.Manager):
    def get_query_set(self):
        return super(BrowsableItemManager, self).get_query_set().filter(parent=None)


class AbstractItem(models.Model):
    """
    The base product object
    """
    # If an item has no parent, then it is the "canonical" or abstract version of a product
    # which essentially represents a set of products.  If a product has a parent
    # then it is a specific version of a product.
    # 
    # For example, a canonical product would have a title like "Green fleece" while its 
    # children would be "Green fleece - size L".
    
    # Universal product code
    upc = models.CharField(max_length=64, blank=True, null=True)
    # No canonical product should have a stock record as they cannot be bought.
    parent = models.ForeignKey('self', null=True, blank=True, related_name='variants',
        help_text="""Only choose a parent product if this is a 'variant' of a canonical product.  For example 
                     if this is a size 4 of a particular t-shirt.  Leave blank if this is a CANONICAL PRODUCT (ie 
                     there is only one version of this product).""")
    # Title is mandatory for canonical products but optional for child products
    title = models.CharField(_('Title'), max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255)
    description = models.TextField(_('Description'), blank=True, null=True)
    item_class = models.ForeignKey('product.ItemClass', verbose_name=_('item class'), null=True,
        help_text="""Choose what type of product this is""")
    attribute_types = models.ManyToManyField('product.AttributeType', through='ItemAttributeValue')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, default=None)

    objects = models.Manager()
    browsable = BrowsableItemManager()

    @property
    def is_top_level(self):
        return self.parent == None
    
    @property
    def is_group(self):
        return self.is_top_level and self.variants.count() > 0
    
    @property
    def is_variant(self):
        return not self.is_top_level

    def attribute_summary(self):
        return ", ".join([attribute.__unicode__() for attribute in self.attributes.all()])

    def get_title(self):
        title = self.__dict__.setdefault('title', '')
        if not title and self.parent_id:
            title = self.parent.title
        return title
    
    def get_item_class(self):
        item_class = self.__dict__.setdefault('item_class', None)
        if not item_class and self.parent_id:
            item_class = self.parent.item_class
        return item_class

    class Meta:
        abstract = True
        ordering = ['-date_created']

    def __unicode__(self):
        if self.is_variant:
            return "%s (%s)" % (self.get_title(), self.attribute_summary())
        return self.get_title()
    
    def get_absolute_url(self):
        args = {'item_class_slug': self.item_class.slug, 
                'item_slug': self.slug,
                'item_id': self.id}
        return reverse('oscar-product-item', kwargs=args)
    
    def save(self, *args, **kwargs):
        if self.is_top_level and not self.title:
            from django.core.exceptions import ValidationError
            raise ValidationError("Canonical products must have a title")
        if not self.slug:
            self.slug = slugify(self.get_title())
        super(AbstractItem, self).save(*args, **kwargs)


class AbstractAttributeType(models.Model):
    """
    Defines an attribute. (Eg. size)
    """
    code = models.CharField(_('code'), max_length=128)
    name = models.CharField(_('name'), max_length=128)
    has_choices = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ['code']

    def __unicode__(self):
        return self.type

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = _convert_to_underscores(self.name)
        super(AbstractAttributeType, self).save(*args, **kwargs)
        

class AbstractAttributeValueOption(models.Model):
    """
    Defines an attribute value choice (Eg: S,M,L,XL for a size attribute type)
    """
    type = models.ForeignKey('product.AttributeType', related_name='options')
    value = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __unicode__(self):
        return "%s = %s" % (self.type, self.value)


class AbstractItemAttributeValue(models.Model):
    """
    A specific attribute value for an item.
    
    Eg: size = L
    """
    product = models.ForeignKey('product.Item', related_name='attributes')
    type = models.ForeignKey('product.AttributeType')
    value = models.CharField(max_length=255)
    
    class Meta:
        abstract = True
        
    def __unicode__(self):
        return "%s: %s" % (self.type.name, self.value)