from django.dispatch import Signal, receiver

order_placed = Signal(providing_args=["order"])

@receiver(order_placed)
def update_stock_levels(sender, **kwargs):
    order = kwargs['order']
    for line in order.lines.all():
        sr = line.product.stockrecord
        sr.decrement_num_in_stock(line.quantity)