from django.shortcuts import render, redirect, get_object_or_404
from .models import PerformanceReview
from .forms import PerformanceReviewForm

def performance_reviews(request):
    """Fetch performance reviews based on user role."""
    user = request.user  # Logged-in user

    if user.is_superuser:  
        # Admin: See reviews where reviewed_by is also an admin
        reviews = PerformanceReview.objects.filter(reviewed_by__is_superuser=True)
    elif user.is_staff:  
        # Manager/Staff: See reviews where they are the reviewer
        reviews = PerformanceReview.objects.filter(reviewed_by=user)
    else:  
        # Regular Employee: See reviews where they are the employee
        reviews = PerformanceReview.objects.filter(employee=user)

    return render(request, 'core/review_list.html', {'reviews': reviews})

def add_review(request):
    """View for adding a new performance review."""
    if request.method == 'POST':
        form = PerformanceReviewForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('review_list')
    else:
        form = PerformanceReviewForm(user=request.user)  # Pass user to form

    return render(request, 'core/add_review.html', {'form': form})

def edit_review(request, review_id):
    review = get_object_or_404(PerformanceReview, pk=review_id)
    if request.method == 'POST':
        form = PerformanceReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('review_list')
    else:
        form = PerformanceReviewForm(instance=review)
    return render(request, 'core/edit_review.html', {'form': form, 'review': review})

def delete_review(request, review_id):
    review = get_object_or_404(PerformanceReview, pk=review_id)
    review.delete()
    return redirect('review_list')
