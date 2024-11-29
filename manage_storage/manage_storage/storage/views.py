from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Item, Category, Shelf, JournalEntry
from .forms import ItemEntryForm, ItemWithdrawalForm, CategoryForm, ShelfForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages


def account_view(request):
    user = request.user  # Получаем текущего пользователя

    return render(request, 'storage/account.html', {
        'user': user,
    })

def item_list(request):
    items = Item.objects.all()
    return render(request, 'storage/item_list.html', {'items': items})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'storage/category_list.html', {'categories': categories})

def shelf_list(request):
    shelves = Shelf.objects.all()
    return render(request, 'storage/shelf_list.html', {'shelves': shelves})

def search_items(request):
    query = request.GET.get('q')
    items = Item.objects.filter(
        name__icontains=query,
        shelf__isnull=False,
        category__isnull=False
    ) if query else []
    return render(request, 'storage/search_results.html', {'items': items})

def home(request):
    return render(request, 'storage/home.html')

def journal_list(request):
    entries = JournalEntry.objects.all().order_by('-timestamp')
    return render(request, 'storage/journal_list.html', {'entries': entries})

def add_item(request):
    if request.method == 'POST':
        item_form = ItemEntryForm(request.POST)
        shelf_id = request.POST.get('shelf')

        if item_form.is_valid():
            item = item_form.save(commit=False)

            if shelf_id:
                shelf = get_object_or_404(Shelf, id=shelf_id)

                if item.size != shelf.size_limit:
                    return render(request, 'storage/add_item.html', {
                        'item_form': item_form,
                        'shelves': Shelf.objects.all().order_by('-capacity'),
                        'error': "Размер товара не соответствует размеру стеллажа."
                    })

                if item.quantity > shelf.capacity:
                    return render(request, 'storage/add_item.html', {
                        'item_form': item_form,
                        'shelves': Shelf.objects.all().order_by('-capacity'),
                        'error': "Недостаточно места на выбранном стеллаже."
                    })

                shelf.capacity -= item.quantity
                shelf.save()

            item.save()
            JournalEntry.objects.create(
                item_name=item.name,
                quantity=item.quantity,
                operation_type='приход',
                data=f"Товар {item.name} добавлен на стеллаж {shelf.name}"
            )
            return redirect('home')

    else:
        item_form = ItemEntryForm()

    shelves = Shelf.objects.all().order_by('-capacity')

    return render(request, 'storage/add_item.html', {
        'item_form': item_form,
        'shelves': shelves,
    })

def withdraw_item(request):
    if request.method == 'POST':
        form = ItemWithdrawalForm(request.POST)

        if form.is_valid():
            item = form.cleaned_data['item']
            quantity = form.cleaned_data['quantity']

            if quantity <= item.quantity:
                item.quantity -= quantity

                JournalEntry.objects.create(
                    item_name=item.name,
                    quantity=quantity,
                    operation_type='уход',
                    data=f"Товар {item.name} выдан со склада"
                )

                if item.quantity == 0:
                    item.delete()
                else:
                    item.save()

                return redirect('home')

            else:
                return render(request, 'storage/withdraw_item.html', {
                    'form': form,
                    'error': "Недостаточно товара на складе."
                })

    else:
        form = ItemWithdrawalForm()

    return render(request, 'storage/withdraw_item.html', {
        'form': form,
    })

def add_category(request):
    if request.method == 'POST':
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            return redirect('item_list')
    else:
        category_form = CategoryForm()

    return render(request, 'storage/add_category.html', {
        'category_form': category_form,
    })

def manage_shelves(request):
    if request.method == 'POST':
        shelf_form = ShelfForm(request.POST)
        if shelf_form.is_valid():
            shelf_form.save()
            return redirect('manage_shelves')

    else:
        shelf_form = ShelfForm()

    shelves = Shelf.objects.all()

    return render(request, 'storage/manage_shelves.html', {
        'shelf_form': shelf_form,
        'shelves': shelves,
    })

def delete_shelf(request, shelf_id):
    shelf = get_object_or_404(Shelf, id=shelf_id)
    shelf.delete()
    return redirect('manage_shelves')