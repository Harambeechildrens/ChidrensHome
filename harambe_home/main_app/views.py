from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Child,Staff,Donor
from .forms import ChildRegistrationForm,StaffRegistrationForm,DonorForm
from .utils import add_to_google_sheet,send_email_notification,delete_from_google_sheet,clear_google_sheet
from django.conf import settings
# Create your views here.



def home(request):
    return render(request, 'index.html')





def register_child(request):
    
    if request.method == "POST":
        form = ChildRegistrationForm(request.POST)
        if form.is_valid():
            last_child = Child.objects.order_by("-child_id").first()
            next_id = 1 if not last_child else last_child.child_id + 1

            child = form.save(commit=False)
            child.child_id = next_id  # ✅ Manually assign ID
            child.save()

            data = [
                child.child_id, child.full_name, child.date_of_birth.strftime("%Y-%m-%d"),
                child.age, child.gender, child.date_of_admission.strftime("%Y-%m-%d"),
                child.reason_for_admission, child.medical_history, child.education_level, child.notes
            ]
            add_to_google_sheet(data, "Children")
            if child.guardian_email:
                subject = "Child Admission Confirmation"
                message = f"Dear Guardian,\n\n{child.full_name} has been successfully admitted to Harambe Children's Home on {child.date_of_admission}.\nIf you have any questions, please contact us.\n\nBest Regards,\nHarambe Children's Home"
                send_email_notification(subject, message, child.guardian_email)

            messages.success(request, "Child added and email sent!")
            return redirect("child_list")
    else:
        form = ChildRegistrationForm()

    return render(request, "dashboard_layout/child_registration.html", {"form": form})


def register_staff(request):
    if request.method == "POST":
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            last_staff = Staff.objects.order_by("-staff_id").first()
            next_id = 1 if not last_staff else last_staff.staff_id + 1

            staff = form.save(commit=False)
            staff.staff_id = next_id  # ✅ Manually assign ID
            staff.save()

            data = [
                staff.staff_id, staff.full_name, staff.role, staff.contact_info,
                staff.date_of_joining.strftime("%Y-%m-%d"), staff.qualifications,
                staff.emergency_contact, staff.notes
            ]
            add_to_google_sheet(data, "Staff")

            subject = "Welcome to Harambe Children's Home"
            message = f"Dear {staff.full_name},\n\nCongratulations on joining Harambe Children's Home as {staff.role}.\nWe look forward to working with you!\n\nBest Regards,\nHarambe Children's Home"
            send_email_notification(subject, message, staff.contact_info)


            messages.success(request, "Staff member added and email sent!")
            return redirect("staff_list")
    else:
        form = StaffRegistrationForm()

    return render(request, "dashboard_layout/staff_registration.html", {"form": form})


@login_required
def dashboard(request):
    total_children = Child.objects.count()
    total_staff = Staff.objects.count()
    total_donors = Donor.objects.count()
    return render(request, "dashboard.html", {"total_children": total_children, "total_staff": total_staff, 'total_donors': total_donors})


def child_list(request):
    children = Child.objects.all()
    return render(request, "child_list.html", {"children": children})

def staff_list(request):
    staff_members = Staff.objects.all()
    return render(request, "staff_list.html", {"staff_members": staff_members})


def reassign_child_ids():
    children = Child.objects.order_by("child_id")
    new_id = 1
    for child in children:
        child.child_id = new_id  # Assign new sequential ID
        child.save()  
        new_id += 1

def reassign_staff_ids():
    staff_members = Staff.objects.order_by("staff_id")
    new_id = 1
    for staff in staff_members:
        staff.staff_id = new_id  # Assign new sequential ID
        staff.save()  # ✅ Save the entire object without `update_fields`
        new_id += 1



def delete_child(request, child_id):
    child = get_object_or_404(Child, child_id=child_id)

    delete_from_google_sheet("Children", child_id)
    child.delete()

    # ✅ Reassign IDs
    reassign_child_ids()

    # ✅ Update Google Sheets
    children = Child.objects.order_by("child_id")
    sheet_data = []
    for child in children:
        data = [
            child.child_id, child.full_name, child.date_of_birth.strftime("%Y-%m-%d"),
            child.age, child.gender, child.date_of_admission.strftime("%Y-%m-%d"),
            child.reason_for_admission, child.medical_history, child.education_level, child.notes
        ]
        sheet_data.append(data)

    clear_google_sheet("Children")
    for row in sheet_data:
        add_to_google_sheet(row, "Children")

    messages.success(request, "Child record deleted, IDs reassigned, and spreadsheet updated!")
    return redirect("child_list")

def delete_staff(request, staff_id):
    staff = get_object_or_404(Staff, staff_id=staff_id)

    # Delete staff from Google Sheets
    delete_from_google_sheet("Staff", staff_id)

    # Delete staff from the database
    staff.delete()

    # Reassign staff IDs in the database
    reassign_staff_ids()

    # Fetch all staff members and update Google Sheets
    staff_members = Staff.objects.order_by("staff_id")
    sheet_data = []
    for staff in staff_members:
        data = [
            staff.staff_id, staff.full_name, staff.role, staff.contact_info,
            staff.date_of_joining.strftime("%Y-%m-%d"), staff.qualifications,
            staff.emergency_contact, staff.notes
        ]
        sheet_data.append(data)

    # Clear and update Google Sheets
    clear_google_sheet("Staff")
    for row in sheet_data:
        add_to_google_sheet(row, "Staff")

    messages.success(request, "Staff record deleted, IDs reassigned, and spreadsheet updated!")
    return redirect("staff_list")

def donor_list(request):
    donors = Donor.objects.all()
    return render(request, 'donor_list.html', {'donors': donors})

def donor_add(request):
    if request.method == "POST":
        form = DonorForm(request.POST)
        if form.is_valid():
            last_donor = Donor.objects.order_by("-donor_id").first()
            next_id = 1 if not last_donor else last_donor.donor_id + 1

            donor = form.save(commit=False)
            donor.donor_id = next_id  
            donor.save()


            data = [
                donor.donor_id, donor.full_name, donor.contact_info,
                str(donor.donation_amount), donor.donation_date.strftime("%Y-%m-%d"),
                donor.donation_type, donor.notes
            ]
            add_to_google_sheet(data, "Donors")


 # ✅ Send email notification to the donor
            subject = "Thank You for Your Donation!"
            message = f"Dear {donor.full_name},\n\nThank you for your generous donation of {donor.donation_amount}.\nWe appreciate your support!\n\nBest Regards,\nHarambe Children's Home"
            send_email_notification(subject, message, donor.contact_info)  # Assuming email is stored in `contact_info`

            messages.success(request, "Donor added and email sent!")
            return redirect("donor_list")
    else:
        form = DonorForm()

    return render(request, "dashboard_layout/donor_form.html", {"form": form})

# def donor_delete(request, donor_id):
#     donor = get_object_or_404(Donor, donor_id=donor_id)

#     delete_from_google_sheet("Donors", donor_id)

#     donor.delete()

#     donors = Donor.objects.order_by("donor_id")
#     new_id = 1
#     sheet_data = []

#     for donor in donors:
#         donor.donor_id = new_id  
#         donor.save(update_fields=["donor_id"])

#         data = [
#             donor.donor_id, donor.full_name, donor.contact_info,
#             str(donor.donation_amount), donor.donation_date.strftime("%Y-%m-%d"),
#             donor.donation_type, donor.notes
#         ]
#         sheet_data.append(data)
#         new_id += 1

    
#     clear_google_sheet("Donors")
#     for row in sheet_data:
#         add_to_google_sheet(row, "Donors")

#     messages.success(request, "Donor deleted, IDs reassigned, and spreadsheet updated!")
#     return redirect("donor_list")

def donor_delete(request, donor_id):
    donor = get_object_or_404(Donor, donor_id=donor_id)  # Use `donor_id` to fetch the donor
    
    # Delete donor from Google Sheets
    delete_from_google_sheet("Donors", donor_id)
    
    # Delete donor from the database
    donor.delete()

    # Fetch all donors and prepare new sheet data
    donors = Donor.objects.order_by("donor_id")  # ✅ Use `donor_id` instead of `id`
    sheet_data = []

    for index, donor in enumerate(donors, start=1):
        # Use `donor.donor_id` for the ID in Google Sheets
        data = [
            index, donor.full_name, donor.contact_info,
            str(donor.donation_amount), donor.donation_date.strftime("%Y-%m-%d"),
            donor.donation_type, donor.notes
        ]
        sheet_data.append(data)

    # Clear and update Google Sheets
    clear_google_sheet("Donors")
    for row in sheet_data:
        add_to_google_sheet(row, "Donors")

    messages.success(request, "Donor deleted, IDs reassigned in Google Sheets, and spreadsheet updated!")
    return redirect("donor_list")