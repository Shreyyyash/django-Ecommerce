# context processors
from .models import Cart
def total_item(request):
    totalitem = Cart.objects.filter(user=request.user.id).count()
    return {'totalitem': totalitem}