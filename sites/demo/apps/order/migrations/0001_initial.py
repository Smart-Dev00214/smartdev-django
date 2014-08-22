# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import oscar.models.fields
import oscar.models.fields.autoslugfield
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('partner', '0001_initial'),
        ('basket', '0001_initial'),
        ('catalogue', '0001_initial'),
        ('customer', '0001_initial'),
        ('sites', '0001_initial'),
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='Title', choices=[('Mr', 'Mr'), ('Miss', 'Miss'), ('Mrs', 'Mrs'), ('Ms', 'Ms'), ('Dr', 'Dr')], blank=True, max_length=64)),
                ('first_name', models.CharField(verbose_name='First name', blank=True, max_length=255)),
                ('last_name', models.CharField(verbose_name='Last name', blank=True, max_length=255)),
                ('line1', models.CharField(verbose_name='First line of address', max_length=255)),
                ('line2', models.CharField(verbose_name='Second line of address', blank=True, max_length=255)),
                ('line3', models.CharField(verbose_name='Third line of address', blank=True, max_length=255)),
                ('line4', models.CharField(verbose_name='City', blank=True, max_length=255)),
                ('state', models.CharField(verbose_name='State/County', blank=True, max_length=255)),
                ('postcode', oscar.models.fields.UppercaseCharField(verbose_name='Post/Zip-code', blank=True, max_length=64)),
                ('search_text', models.TextField(editable=False, verbose_name='Search text - used only for searching addresses')),
                ('country', models.ForeignKey(verbose_name='Country', to='address.Country')),
            ],
            options={
                'verbose_name': 'Billing address',
                'verbose_name_plural': 'Billing addresses',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CommunicationEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(verbose_name='Date', auto_now_add=True)),
                ('event_type', models.ForeignKey(verbose_name='Event Type', to='customer.CommunicationEventType')),
            ],
            options={
                'verbose_name': 'Communication Event',
                'verbose_name_plural': 'Communication Events',
                'ordering': ['-date_created'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('partner_name', models.CharField(verbose_name='Partner name', blank=True, max_length=128)),
                ('partner_sku', models.CharField(verbose_name='Partner SKU', max_length=128)),
                ('partner_line_reference', models.CharField(verbose_name='Partner reference', blank=True, help_text='This is the item number that the partner uses within their system', max_length=128)),
                ('partner_line_notes', models.TextField(verbose_name='Partner Notes', blank=True)),
                ('title', models.CharField(verbose_name='Title', max_length=255)),
                ('upc', models.CharField(verbose_name='UPC', blank=True, null=True, max_length=128)),
                ('quantity', models.PositiveIntegerField(verbose_name='Quantity', default=1)),
                ('line_price_incl_tax', models.DecimalField(verbose_name='Price (inc. tax)', max_digits=12, decimal_places=2)),
                ('line_price_excl_tax', models.DecimalField(verbose_name='Price (excl. tax)', max_digits=12, decimal_places=2)),
                ('line_price_before_discounts_incl_tax', models.DecimalField(verbose_name='Price before discounts (inc. tax)', max_digits=12, decimal_places=2)),
                ('line_price_before_discounts_excl_tax', models.DecimalField(verbose_name='Price before discounts (excl. tax)', max_digits=12, decimal_places=2)),
                ('unit_cost_price', models.DecimalField(verbose_name='Unit Cost Price', max_digits=12, decimal_places=2, blank=True, null=True)),
                ('unit_price_incl_tax', models.DecimalField(verbose_name='Unit Price (inc. tax)', max_digits=12, decimal_places=2, blank=True, null=True)),
                ('unit_price_excl_tax', models.DecimalField(verbose_name='Unit Price (excl. tax)', max_digits=12, decimal_places=2, blank=True, null=True)),
                ('unit_retail_price', models.DecimalField(verbose_name='Unit Retail Price', max_digits=12, decimal_places=2, blank=True, null=True)),
                ('status', models.CharField(verbose_name='Status', blank=True, max_length=255)),
                ('est_dispatch_date', models.DateField(verbose_name='Estimated Dispatch Date', blank=True, null=True)),
                ('partner', models.ForeignKey(verbose_name='Partner', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='partner.Partner', null=True)),
                ('product', models.ForeignKey(verbose_name='Product', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='catalogue.Product', null=True)),
                ('stockrecord', models.ForeignKey(verbose_name='Stock record', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='partner.StockRecord', null=True)),
            ],
            options={
                'verbose_name': 'Order Line',
                'verbose_name_plural': 'Order Lines',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LineAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('type', models.CharField(verbose_name='Type', max_length=128)),
                ('value', models.CharField(verbose_name='Value', max_length=255)),
                ('line', models.ForeignKey(verbose_name='Line', to='order.Line')),
                ('option', models.ForeignKey(verbose_name='Option', on_delete=django.db.models.deletion.SET_NULL, to='catalogue.Option', null=True)),
            ],
            options={
                'verbose_name': 'Line Attribute',
                'verbose_name_plural': 'Line Attributes',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LinePrice',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField(verbose_name='Quantity', default=1)),
                ('price_incl_tax', models.DecimalField(verbose_name='Price (inc. tax)', max_digits=12, decimal_places=2)),
                ('price_excl_tax', models.DecimalField(verbose_name='Price (excl. tax)', max_digits=12, decimal_places=2)),
                ('shipping_incl_tax', models.DecimalField(verbose_name='Shiping (inc. tax)', max_digits=12, decimal_places=2, default=0)),
                ('shipping_excl_tax', models.DecimalField(verbose_name='Shipping (excl. tax)', max_digits=12, decimal_places=2, default=0)),
                ('line', models.ForeignKey(verbose_name='Line', to='order.Line')),
            ],
            options={
                'verbose_name': 'Line Price',
                'verbose_name_plural': 'Line Prices',
                'ordering': ('id',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('number', models.CharField(verbose_name='Order number', unique=True, db_index=True, max_length=128)),
                ('currency', models.CharField(verbose_name='Currency', default='GBP', max_length=12)),
                ('total_incl_tax', models.DecimalField(verbose_name='Order total (inc. tax)', max_digits=12, decimal_places=2)),
                ('total_excl_tax', models.DecimalField(verbose_name='Order total (excl. tax)', max_digits=12, decimal_places=2)),
                ('shipping_incl_tax', models.DecimalField(verbose_name='Shipping charge (inc. tax)', max_digits=12, decimal_places=2, default=0)),
                ('shipping_excl_tax', models.DecimalField(verbose_name='Shipping charge (excl. tax)', max_digits=12, decimal_places=2, default=0)),
                ('shipping_method', models.CharField(verbose_name='Shipping method', blank=True, max_length=128)),
                ('shipping_code', models.CharField(blank=True, default='', max_length=128)),
                ('status', models.CharField(verbose_name='Status', blank=True, max_length=100)),
                ('guest_email', models.EmailField(verbose_name='Guest email address', blank=True, max_length=75)),
                ('date_placed', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('basket', models.ForeignKey(verbose_name='Basket', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='basket.Basket', null=True)),
                ('billing_address', models.ForeignKey(verbose_name='Billing Address', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='order.BillingAddress', null=True)),
                ('site', models.ForeignKey(verbose_name='Site', on_delete=django.db.models.deletion.SET_NULL, to='sites.Site', null=True)),
                ('user', models.ForeignKey(verbose_name='User', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'ordering': ['-date_placed'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='lineprice',
            name='order',
            field=models.ForeignKey(verbose_name='Option', to='order.Order'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='line',
            name='order',
            field=models.ForeignKey(verbose_name='Order', to='order.Order'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='communicationevent',
            name='order',
            field=models.ForeignKey(verbose_name='Order', to='order.Order'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='OrderDiscount',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('category', models.CharField(verbose_name='Discount category', choices=[('Basket', 'Basket'), ('Shipping', 'Shipping'), ('Deferred', 'Deferred')], default='Basket', max_length=64)),
                ('offer_id', models.PositiveIntegerField(verbose_name='Offer ID', blank=True, null=True)),
                ('offer_name', models.CharField(verbose_name='Offer name', blank=True, db_index=True, max_length=128)),
                ('voucher_id', models.PositiveIntegerField(verbose_name='Voucher ID', blank=True, null=True)),
                ('voucher_code', models.CharField(verbose_name='Code', blank=True, db_index=True, max_length=128)),
                ('frequency', models.PositiveIntegerField(verbose_name='Frequency', null=True)),
                ('amount', models.DecimalField(verbose_name='Amount', max_digits=12, decimal_places=2, default=0)),
                ('message', models.TextField(blank=True)),
                ('order', models.ForeignKey(verbose_name='Order', to='order.Order')),
            ],
            options={
                'verbose_name': 'Order Discount',
                'verbose_name_plural': 'Order Discounts',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderNote',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('note_type', models.CharField(verbose_name='Note Type', blank=True, max_length=128)),
                ('message', models.TextField(verbose_name='Message')),
                ('date_created', models.DateTimeField(verbose_name='Date Created', auto_now_add=True)),
                ('date_updated', models.DateTimeField(verbose_name='Date Updated', auto_now=True)),
                ('order', models.ForeignKey(verbose_name='Order', to='order.Order')),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Order Note',
                'verbose_name_plural': 'Order Notes',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PaymentEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('amount', models.DecimalField(verbose_name='Amount', max_digits=12, decimal_places=2)),
                ('reference', models.CharField(verbose_name='Reference', blank=True, max_length=128)),
                ('date_created', models.DateTimeField(verbose_name='Date created', auto_now_add=True)),
                ('order', models.ForeignKey(verbose_name='Order', to='order.Order')),
            ],
            options={
                'verbose_name': 'Payment Event',
                'verbose_name_plural': 'Payment Events',
                'ordering': ['-date_created'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PaymentEventQuantity',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField(verbose_name='Quantity')),
            ],
            options={
                'verbose_name': 'Payment Event Quantity',
                'verbose_name_plural': 'Payment Event Quantities',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='paymentevent',
            name='lines',
            field=models.ManyToManyField(verbose_name='Lines', through='order.PaymentEventQuantity', to='order.Line'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='paymenteventquantity',
            name='event',
            field=models.ForeignKey(verbose_name='Event', to='order.PaymentEvent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='paymenteventquantity',
            name='line',
            field=models.ForeignKey(verbose_name='Line', to='order.Line'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='paymenteventquantity',
            unique_together=set([('event', 'line')]),
        ),
        migrations.CreateModel(
            name='PaymentEventType',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='Name', unique=True, max_length=128)),
                ('code', oscar.models.fields.autoslugfield.AutoSlugField(editable=False, verbose_name='Code', blank=True, max_length=128, populate_from='name', unique=True)),
            ],
            options={
                'verbose_name': 'Payment Event Type',
                'verbose_name_plural': 'Payment Event Types',
                'ordering': ('name',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='paymentevent',
            name='event_type',
            field=models.ForeignKey(verbose_name='Event Type', to='order.PaymentEventType'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='Title', choices=[('Mr', 'Mr'), ('Miss', 'Miss'), ('Mrs', 'Mrs'), ('Ms', 'Ms'), ('Dr', 'Dr')], blank=True, max_length=64)),
                ('first_name', models.CharField(verbose_name='First name', blank=True, max_length=255)),
                ('last_name', models.CharField(verbose_name='Last name', blank=True, max_length=255)),
                ('line1', models.CharField(verbose_name='First line of address', max_length=255)),
                ('line2', models.CharField(verbose_name='Second line of address', blank=True, max_length=255)),
                ('line3', models.CharField(verbose_name='Third line of address', blank=True, max_length=255)),
                ('line4', models.CharField(verbose_name='City', blank=True, max_length=255)),
                ('state', models.CharField(verbose_name='State/County', blank=True, max_length=255)),
                ('postcode', oscar.models.fields.UppercaseCharField(verbose_name='Post/Zip-code', blank=True, max_length=64)),
                ('search_text', models.TextField(editable=False, verbose_name='Search text - used only for searching addresses')),
                ('phone_number', oscar.models.fields.PhoneNumberField(verbose_name='Phone number', blank=True, help_text='In case we need to call you about your order')),
                ('notes', models.TextField(verbose_name='Instructions', blank=True, help_text='Tell us anything we should know when delivering your order.')),
                ('country', models.ForeignKey(verbose_name='Country', to='address.Country')),
            ],
            options={
                'verbose_name': 'Shipping address',
                'verbose_name_plural': 'Shipping addresses',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(verbose_name='Shipping Address', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='order.ShippingAddress', null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='ShippingEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('notes', models.TextField(verbose_name='Event notes', blank=True, help_text='This could be the dispatch reference, or a tracking number')),
                ('date_created', models.DateTimeField(verbose_name='Date Created', auto_now_add=True)),
                ('order', models.ForeignKey(verbose_name='Order', to='order.Order')),
            ],
            options={
                'verbose_name': 'Shipping Event',
                'verbose_name_plural': 'Shipping Events',
                'ordering': ['-date_created'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='paymentevent',
            name='shipping_event',
            field=models.ForeignKey(to='order.ShippingEvent', null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='ShippingEventQuantity',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField(verbose_name='Quantity')),
            ],
            options={
                'verbose_name': 'Shipping Event Quantity',
                'verbose_name_plural': 'Shipping Event Quantities',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='shippingevent',
            name='lines',
            field=models.ManyToManyField(verbose_name='Lines', through='order.ShippingEventQuantity', to='order.Line'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shippingeventquantity',
            name='event',
            field=models.ForeignKey(verbose_name='Event', to='order.ShippingEvent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shippingeventquantity',
            name='line',
            field=models.ForeignKey(verbose_name='Line', to='order.Line'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='shippingeventquantity',
            unique_together=set([('event', 'line')]),
        ),
        migrations.CreateModel(
            name='ShippingEventType',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='Name', unique=True, max_length=255)),
                ('code', oscar.models.fields.autoslugfield.AutoSlugField(editable=False, verbose_name='Code', blank=True, max_length=128, populate_from='name', unique=True)),
            ],
            options={
                'verbose_name': 'Shipping Event Type',
                'verbose_name_plural': 'Shipping Event Types',
                'ordering': ('name',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='shippingevent',
            name='event_type',
            field=models.ForeignKey(verbose_name='Event Type', to='order.ShippingEventType'),
            preserve_default=True,
        ),
    ]
