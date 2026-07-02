from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import LostItemForm, FoundItemForm
from .matching import find_matches_for_lost, find_matches_for_found
from .models import LostItem, FoundItem, Notification, CATEGORY_CHOICES


def home_view(request):
    recent_lost = LostItem.objects.filter(status='active').order_by('-created_at')[:4]
    recent_found = FoundItem.objects.filter(status='active').order_by('-created_at')[:4]
    context = {
        'recent_lost': recent_lost,
        'recent_found': recent_found,
        'total_lost': LostItem.objects.count(),
        'total_found': FoundItem.objects.count(),
        'total_returned': LostItem.objects.filter(status='found').count() + FoundItem.objects.filter(status='returned').count(),
        'total_users': get_user_model().objects.count(),
    }
    return render(request, 'items/home.html', context)


def about_view(request):
    return render(request, 'items/about.html')


def contact_view(request):
    if request.method == 'POST':
        messages.success(request, "Thanks for reaching out! Our team will get back to you soon.")
        return redirect('items:contact')
    return render(request, 'items/contact.html')


@login_required
def dashboard_view(request):
    user = request.user
    my_lost = LostItem.objects.filter(owner=user)
    my_found = FoundItem.objects.filter(finder=user)

    recent_posts = sorted(
        list(LostItem.objects.order_by('-created_at')[:5]) + list(FoundItem.objects.order_by('-created_at')[:5]),
        key=lambda x: x.created_at, reverse=True
    )[:6]

    context = {
        'total_lost': LostItem.objects.filter(status='active').count(),
        'total_found': FoundItem.objects.filter(status='active').count(),
        'total_returned': LostItem.objects.filter(status='found').count() + FoundItem.objects.filter(status='returned').count(),
        'my_lost_count': my_lost.count(),
        'my_found_count': my_found.count(),
        'recent_posts': recent_posts,
        'unread_notifications': Notification.objects.filter(user=user, is_read=False).count(),
    }
    return render(request, 'items/dashboard.html', context)


def _apply_filters(request, qs, date_field):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '')
    location = request.GET.get('location', '').strip()
    date = request.GET.get('date', '')
    sort = request.GET.get('sort', 'recent')

    if query:
        qs = qs.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category:
        qs = qs.filter(category=category)
    if location:
        qs = qs.filter(location__icontains=location)
    if date:
        qs = qs.filter(**{date_field: date})

    if sort == 'recent':
        qs = qs.order_by('-created_at')
    elif sort == 'oldest':
        qs = qs.order_by('created_at')

    return qs


def lost_items_view(request):
    qs = LostItem.objects.all()
    status_filter = request.GET.get('status', 'active')
    if status_filter == 'active':
        qs = qs.filter(status='active')
    elif status_filter == 'found':
        qs = qs.filter(status='found')

    qs = _apply_filters(request, qs, 'date_lost')
    paginator = Paginator(qs, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'categories': CATEGORY_CHOICES,
        'status_filter': status_filter,
        'query': request.GET.get('q', ''),
    }
    return render(request, 'items/lost_items.html', context)


def found_items_view(request):
    qs = FoundItem.objects.all()
    status_filter = request.GET.get('status', 'active')
    if status_filter == 'active':
        qs = qs.filter(status='active')
    elif status_filter == 'returned':
        qs = qs.filter(status='returned')

    qs = _apply_filters(request, qs, 'date_found')
    paginator = Paginator(qs, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'categories': CATEGORY_CHOICES,
        'status_filter': status_filter,
        'query': request.GET.get('q', ''),
    }
    return render(request, 'items/found_items.html', context)


def search_api_view(request):
    """Real-time search endpoint used by the navbar search box (AJAX)."""
    query = request.GET.get('q', '').strip()
    results = []
    if len(query) >= 2:
        lost = LostItem.objects.filter(Q(title__icontains=query) | Q(description__icontains=query), status='active')[:5]
        found = FoundItem.objects.filter(Q(title__icontains=query) | Q(description__icontains=query), status='active')[:5]
        for item in lost:
            results.append({'title': item.title, 'type': 'Lost', 'url': item.get_absolute_url(), 'location': item.location})
        for item in found:
            results.append({'title': item.title, 'type': 'Found', 'url': item.get_absolute_url(), 'location': item.location})
    return JsonResponse({'results': results})


@login_required
def create_lost_view(request):
    if request.method == 'POST':
        form = LostItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            matches = find_matches_for_lost(item, FoundItem.objects.all())
            if matches:
                Notification.objects.create(
                    user=request.user,
                    message=f'Potential match found for your lost "{item.title}"!',
                    notif_type='match',
                    link=item.get_absolute_url(),
                )
            messages.success(request, "Lost item reported successfully!")
            return redirect('items:lost_detail', pk=item.pk)
        messages.error(request, "Please fix the errors below.")
    else:
        form = LostItemForm()
    return render(request, 'items/item_form.html', {'form': form, 'form_title': 'Report Lost Item', 'kind': 'lost'})


@login_required
def create_found_view(request):
    if request.method == 'POST':
        form = FoundItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.finder = request.user
            item.save()
            matches = find_matches_for_found(item, LostItem.objects.all())
            if matches:
                Notification.objects.create(
                    user=request.user,
                    message=f'Potential match found for your found "{item.title}"!',
                    notif_type='match',
                    link=item.get_absolute_url(),
                )
                for lost_item, score in matches:
                    Notification.objects.create(
                        user=lost_item.owner,
                        message=f'Potential match found for your lost "{lost_item.title}"!',
                        notif_type='match',
                        link=lost_item.get_absolute_url(),
                    )
            messages.success(request, "Found item reported successfully! Thank you for helping a fellow student.")
            return redirect('items:found_detail', pk=item.pk)
        messages.error(request, "Please fix the errors below.")
    else:
        form = FoundItemForm()
    return render(request, 'items/item_form.html', {'form': form, 'form_title': 'Report Found Item', 'kind': 'found'})


@login_required
def edit_lost_view(request, pk):
    item = get_object_or_404(LostItem, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = LostItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Lost item report updated.")
            return redirect('items:lost_detail', pk=item.pk)
    else:
        form = LostItemForm(instance=item)
    return render(request, 'items/item_form.html', {'form': form, 'form_title': 'Edit Lost Item', 'kind': 'lost', 'editing': True})


@login_required
def edit_found_view(request, pk):
    item = get_object_or_404(FoundItem, pk=pk, finder=request.user)
    if request.method == 'POST':
        form = FoundItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Found item report updated.")
            return redirect('items:found_detail', pk=item.pk)
    else:
        form = FoundItemForm(instance=item)
    return render(request, 'items/item_form.html', {'form': form, 'form_title': 'Edit Found Item', 'kind': 'found', 'editing': True})


@login_required
def delete_lost_view(request, pk):
    item = get_object_or_404(LostItem, pk=pk, owner=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Lost item report deleted.")
        return redirect('items:lost_items')
    return render(request, 'items/confirm_delete.html', {'item': item})


@login_required
def delete_found_view(request, pk):
    item = get_object_or_404(FoundItem, pk=pk, finder=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Found item report deleted.")
        return redirect('items:found_items')
    return render(request, 'items/confirm_delete.html', {'item': item})


@login_required
def mark_lost_found_view(request, pk):
    item = get_object_or_404(LostItem, pk=pk, owner=request.user)
    item.status = 'found'
    item.save()
    messages.success(request, f'"{item.title}" marked as found. Glad it turned up!')
    return redirect('items:lost_detail', pk=item.pk)


@login_required
def mark_found_returned_view(request, pk):
    item = get_object_or_404(FoundItem, pk=pk, finder=request.user)
    item.status = 'returned'
    item.save()
    Notification.objects.create(
        user=request.user,
        message=f'"{item.title}" marked as returned. Thanks for helping reunite it with its owner!',
        notif_type='returned',
        link=item.get_absolute_url(),
    )
    messages.success(request, f'"{item.title}" marked as returned.')
    return redirect('items:found_detail', pk=item.pk)


def lost_detail_view(request, pk):
    item = get_object_or_404(LostItem, pk=pk)
    matches = find_matches_for_lost(item, FoundItem.objects.all())
    return render(request, 'items/item_detail.html', {'item': item, 'kind': 'lost', 'matches': matches})


def found_detail_view(request, pk):
    item = get_object_or_404(FoundItem, pk=pk)
    matches = find_matches_for_found(item, LostItem.objects.all())
    return render(request, 'items/item_detail.html', {'item': item, 'kind': 'found', 'matches': matches})


@login_required
def report_match_view(request, kind, pk):
    """User confirms a suggested match is genuinely theirs."""
    if kind == 'lost':
        item = get_object_or_404(LostItem, pk=pk)
        recipient = item.owner
    else:
        item = get_object_or_404(FoundItem, pk=pk)
        recipient = item.finder

    Notification.objects.create(
        user=recipient,
        message=f'{request.user.get_full_name() or request.user.username} reported a match on your "{item.title}" post!',
        notif_type='match',
        link=item.get_absolute_url(),
    )
    messages.success(request, "Match reported! We've notified the poster.")
    return redirect(item.get_absolute_url())


@login_required
def mark_notification_read_view(request, pk):
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    if notif.link:
        return redirect(notif.link)
    return redirect('items:dashboard')


@login_required
def admin_dashboard_view(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to view the admin dashboard.")
        return redirect('items:dashboard')

    User = get_user_model()
    context = {
        'total_users': User.objects.count(),
        'total_lost': LostItem.objects.count(),
        'total_found': FoundItem.objects.count(),
        'total_returned': LostItem.objects.filter(status='found').count() + FoundItem.objects.filter(status='returned').count(),
        'active_lost': LostItem.objects.filter(status='active').count(),
        'active_found': FoundItem.objects.filter(status='active').count(),
        'recent_lost': LostItem.objects.order_by('-created_at')[:6],
        'recent_found': FoundItem.objects.order_by('-created_at')[:6],
        'recent_users': User.objects.order_by('-created_at')[:6],
    }
    return render(request, 'items/admin_dashboard.html', context)


@login_required
def notifications_view(request):
    notifs = Notification.objects.filter(user=request.user)
    notifs.filter(is_read=False).update(is_read=True)
    return render(request, 'items/notifications.html', {'notifications': notifs})
