from django.conf import settings

from Stores.models import Product_info, Service_info


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product_info.objects.get(pk=p)

        for item in self.cart.values():
            item['total_price'] = int(item['product'].product_price * item['quantity']) / 100

            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self, pk, quantity=1, update_quantity=False):
        product_id = str(pk)

        if product_id not in self.cart:
            self.cart[pk] = {'quantity': int(quantity), 'id': pk}

        if update_quantity:
            self.cart[pk]['quantity'] += int(quantity)

            if self.cart[pk]['quantity'] == 0:
                self.remove(pk)

        self.save()

    def remove(self, pk):
        if str(pk) in self.cart:
            del self.cart[str(pk)]

            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total_cost(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product_info.objects.get(pk=p)

        return int(sum(item['product'].product_price * item['quantity'] for item in self.cart.values()))