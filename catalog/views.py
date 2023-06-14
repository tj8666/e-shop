from django.shortcuts import render, redirect
from . import models
from . import handlers
# from django.http import HttpResponse
# Create your views here.
def main_page(request):
    # Получаем все данные о категориях из базы
    all_categories = models.Category.objects.all()
    all_products = models.Product.objects.all()
    #Получить переменную из фронт части, если она есть
    search_value_from_front = request.GET.get('search')
    if search_value_from_front:
        all_products = models.Product.objects.filter(name__contains=search_value_from_front)

    #Передача переменных из бека на фронт
    context = {'all_categories':all_categories, 'all_products':all_products}
    return render(request, 'index.html', context)

#  Получить продукты из конкретно категории
def get_category_products(request, pk):
    # Получить все товары из конкретной категории
    exact_category_products = models.Product.objects.filter(category_name__id=pk)
    context = {'category_products': exact_category_products}
    return render(request, 'category.html', context)

# Функция получения определенного продукта
def get_products(request, name, pk):

    exact_products = models.Product.objects.get(name=name, id=pk)
    # Передаем переменные из бека на фронт
    context = {'product': exact_products}
    return render(request, 'product.html', context)

# Функция добавления продукта в корзину
def add_pr_to_cart(request, pk):
    # Получить выбранное количество продукта из фронт части
    quantity = request.POST.get('pr_count')
    # Находим продукт из базы
    product_to_add = models.Product.objects.get(id=pk)
    # Добавление данных
    models.UserCart.objects.create(user_id=request.user.id,
                                   user_product=product_to_add,
                                   user_product_quantity=quantity)
    return redirect('/')
#
def get_user_cart(request):
    products_from_cart = models.UserCart.objects.filter(user_id=request.user.id)
    context = {'cart_products': products_from_cart}
    return render(request, 'cart.html', context)

def complete_order(request):
    # Получаем корзину пользователя
    user_cart = models.UserCart.objects.filter(user_id=request.user.id)
    # Собираем сообщение бота для админа
    if request.method == 'POST':
        tg_message = 'Новый заказ с (сайта)\n\n'
        total = 0
        for cart in user_cart:
            tg_message += f'Название товара{cart.user_product}\n' \
                      f'Количество: {cart.user_product_quantity}\n'
            total += cart.user_product.price * cart.user_product_quantity
        tg_message += f'Итог: {total}'
        handlers.bot.send_message(117657882, tg_message)
        #
        user_cart.delete()
        return redirect('/')
    return render(request, 'cart.html', {'user_cart': user_cart})
# функция очистки корзины
def delete_from_user_cart(request, pk):
    product_to_delete = models.Product.objects.get(id=pk)
    models.UserCart.objects.filter(user_id=request.user.id, user_product=product_to_delete).delete()
    return redirect('/cart')

def about_page(request):
    return render(request, 'about.html')
def faq(request):
    return render(request, 'faq.html')

#    return HttpResponse('If you have any questions<br>we dont give a fuck<br> just suck our dick')

