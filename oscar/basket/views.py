import zlib

from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseBadRequest
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse

from oscar.basket.models import Basket
from oscar.basket.forms import AddToBasketForm
from oscar.product.models import Item

COOKIE_KEY_ID = 'basket_id'
COOKIE_KEY_HASH = 'basket_hash'
COOKIE_LIFETIME = 7*24*60*60

def _get_user_basket(request):
    b = None
    if request.user.is_authenticated():
        # @todo user baskets
        pass
    else:
        # If user is anonymous, their basket ID (if they have one) will be
        # stored in a cookie together with a hash which verifies it and prevents
        # it from being spoofed.
        if request.COOKIES.has_key(COOKIE_KEY_ID) and request.COOKIES.has_key(COOKIE_KEY_HASH):
            basket_id = request.COOKIES[COOKIE_KEY_ID]
            basket_hash = request.COOKIES[COOKIE_KEY_HASH]
            if basket_hash == _get_basket_hash(basket_id):
                b = Basket.objects.get(pk=request.COOKIES[COOKIE_KEY_ID])
    return b    

def _get_or_create_basket(request, response):
    """
    Loads or creates a basket object
    
    If the user is anonymous, the id of the basket is stored in
    a cookie.
    """
    b = _get_user_basket(request)
    if not b and not request.user.is_authenticated():
        # No valid basket found so we create a new one and store the id
        # and hash in a cookie
        b = Basket.objects.create()
        response.set_cookie(COOKIE_KEY_ID, b.pk, max_age=COOKIE_LIFETIME)
        response.set_cookie(COOKIE_KEY_HASH, _get_basket_hash(b.pk), max_age=COOKIE_LIFETIME)
    return b    

def _get_basket_hash(id):
    """
    Create a hash of the basket ID using the SECRET_KEY
    variable defined in settings.py as a salt.
    """
    return zlib.crc32(str(id)+settings.SECRET_KEY)

def index(request):
    """ 
    Pages should POST to this view to add an item to someone's basket
    """
    if request.method == 'POST': 
        form = AddToBasketForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest("Unable to add your item to the basket")
        try:
            # We create the response object early as the basket creation
            # may need to set a cookie on it
            response = HttpResponseRedirect('/shop/basket/')
            product = Item.objects.get(pk=form.cleaned_data['product_id'])
            basket = _get_or_create_basket(request, response)
            basket.add_product(product)
        except Item.DoesNotExist, e:
            response = HttpResponseBadRequest("Unable to find the requested item to add to your basket")
        except Basket.DoesNotExist, e:
            response = HttpResponseBadRequest("Unable to find your basket") 
    else:
        # Display the visitor's basket
        basket = _get_user_basket(request)
        if not basket:
            basket = Basket()
        response = render_to_response('basket.html', locals(), context_instance=RequestContext(request))
    return response
