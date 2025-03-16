from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Leave, LeaveQuota
from .forms import LeaveApplicationForm, LeaveApprovalForm
from employe.models import Employe_User

@login_required
def apply_leave(request):
    if request.method == "POST":
        form = LeaveApplicationForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user  # Assign logged-in employee
            leave.status = 'pending'
            leave.save()
            return redirect('leave_status')
    else:
        form = LeaveApplicationForm()
    return render(request, 'core/apply_leave.html', {'form': form})

@login_required
def leave_status(request):
    leaves = Leave.objects.filter(employee=request.user)
    return render(request, 'core/leave_status.html', {'leaves': leaves})

@login_required
def approve_leave(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)
    if request.method == "POST":
        form = LeaveApprovalForm(request.POST, instance=leave)
        if form.is_valid():
            approved_leave = form.save(commit=False)
            approved_leave.approved_by = request.user  # Admin approving
            approved_leave.save()

            # Update Leave Quota if approved
            if approved_leave.status == 'approved':
                quota = LeaveQuota.objects.get(employee=approved_leave.employee, leave_type=approved_leave.leave_type)
                quota.used_quota += approved_leave.total_days
                quota.remain_quota -= approved_leave.total_days
                quota.save()

            return redirect('admin_dashboard')
    else:
        form = LeaveApprovalForm(instance=leave)
    return render(request, 'core/approve_leave.html', {'form': form, 'leave': leave})
