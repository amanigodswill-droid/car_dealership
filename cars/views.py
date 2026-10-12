from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.core.serializers import python
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CarForm, RegisterForm, SellerProfileForm, CustomerReviewForm, CarSaleForm
from .models import Car, SellerProfile , CustomerReview, CarSale
    
def car_list(request):
    cars = Car.objects.all()
    return render(request, 'cars/car_list.html', {'cars': cars})


def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    seller_profile, created = SellerProfile.objects.get_or_create(user=car.seller)
    reviews = CustomerReview.objects.filter(seller=car.seller).select_related('customer')
    can_review = False

    if request.user.is_authenticated and request.user != car.seller:
        completed_purchase = CarSale.objects.filter(buyer=request.user, seller=car.seller, status='completed').exists()
        existing_review = CustomerReview.objects.filter(customer=request.user,seller=car.seller).exists()
        can_review = completed_purchase and not existing_review

    return render(request, 'cars/car_detail.html', {
        'car': car,
        'seller_profile': seller_profile,
        'reviews': reviews,
        'can_review': can_review,
    })

@login_required
def car_create(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        car = form.save(commit=False)
        car.seller = request.user
        car.save()
        return redirect('car_list')
    else:
        form = CarForm()
    return render(request, 'cars/car_form.html', {'form': form})

@login_required
def car_update(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if car.seller != request.user:
        return redirect('car_detail', pk=car.pk)

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('car_detail', pk=car.pk)
    else:
        form = CarForm(instance=car)

    return render(request, 'cars/car_form.html', {
        'form': form,
        'car': car
    })

@login_required
def car_delete(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if car.seller != request.user:
        return redirect('car_detail', pk=car.pk)
    if request.method == 'POST':
        car.delete()
        return redirect('car_list')

    return render(request, 'cars/car_confirm_delete.html', {
        'car': car
    })
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('car_list')
    else:
        form = RegisterForm()
    return render(request, 'cars/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('car_list')
    else:
        form = AuthenticationForm()
    return render(request, 'cars/login.html', {'form': form})


@login_required
def seller_profile(request):
    profile, created = SellerProfile.objects.get_or_create(
        user=request.user)

    if request.method == 'POST':
        form = SellerProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('seller_profile')
    else:
        form = SellerProfileForm(instance=profile)

    return render(request, 'cars/seller_profile.html', {
        'form': form
    })


@login_required
def car_inquire(request, pk):
    car = get_object_or_404(Car, pk=pk)
    seller_profile, created = SellerProfile.objects.get_or_create(user=car.seller)
    return render(request, 'cars/car_inquire.html', {
        'car': car,
        'seller_profile': seller_profile
    })


@login_required
def car_review(request, pk):
    car = get_object_or_404(Car, pk=pk)
    seller = car.seller

    if seller == request.user:
        return redirect('car_detail', pk=car.pk)

    completed_purchase = CarSale.objects.filter(buyer=request.user,seller=seller, status='completed').exists()
   
    if not completed_purchase:
        return redirect('car_detail', pk=car.pk)

    existing_review = CustomerReview.objects.filter(customer=request.user, seller=seller).first()

    if existing_review:
        return redirect('car_detail', pk=car.pk)

    if request.method == 'POST':
        form = CustomerReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.customer = request.user
            review.seller = seller
            review.save()

            return redirect('car_detail', pk=car.pk)
    else:
        form = CustomerReviewForm()

    return render(request, 'cars/car_review.html', {
        'form': form,
        'car': car,
    })

@login_required
def car_purchase_request(request, pk):
    car = get_object_or_404(Car, pk=pk)

    if car.seller == request.user:
        return redirect('car_detail', pk=car.pk)
    active_sale = CarSale.objects.filter(
        car=car,
        status__in=['pending', 'completed']
    ).exists()

    if active_sale:
        return redirect('car_detail', pk=car.pk)

    if request.method == 'POST':
        form = CarSaleForm(request.POST)

        if form.is_valid():
            sale = form.save(commit=False)
            sale.car = car
            sale.buyer = request.user
            sale.seller = car.seller
            sale.status = 'pending'
            sale.save()

            return redirect('car_detail', pk=car.pk)
    else:
        form = CarSaleForm()

    return render(request, 'cars/car_sale_request.html', {
        'form': form,
        'car': car,
    })

@login_required
def seller_sale_requests(request):
    sales = CarSale.objects.filter(
        seller=request.user
    ).select_related('car', 'buyer').order_by('-date_created')

    return render(request, 'cars/seller_sale_requests.html', {
        'sales': sales,
    })

@login_required
def update_sale_status(request, sale_id):
    sale = get_object_or_404(CarSale,pk=sale_id,seller=request.user)

    if request.method == 'POST':
        status = request.POST.get('status')

        if status in ['completed', 'cancelled']:
            if status == 'completed':
                existing_sale = CarSale.objects.filter(
                    car=sale.car,
                    status='completed'
                ).exclude(pk=sale.pk).exists()

                if existing_sale:
                    return redirect('seller_sale_requests')

            sale.status = status
            sale.save()

    return redirect('seller_sale_requests')