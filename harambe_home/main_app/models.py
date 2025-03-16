from django.db import models

# Create your models here.

from django.db import models

class Child(models.Model):
    child_id = models.IntegerField(primary_key=True) 
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[("Male", "Male"), ("Female", "Female")])
    date_of_admission = models.DateField()
    reason_for_admission = models.TextField()
    medical_history = models.TextField(blank=True, null=True)
    education_level = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    guardian_email = models.EmailField(blank=True, null=True)  # For email notifications

    def __str__(self):
        return f"{self.child_id} - {self.full_name}"

class Staff(models.Model):
    staff_id = models.IntegerField(primary_key=True)  
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    contact_info = models.EmailField()
    date_of_joining = models.DateField()
    qualifications = models.TextField()
    emergency_contact = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.staff_id} - {self.full_name}"
    

class Donor(models.Model):
    donor_id = models.IntegerField(primary_key=True)
    full_name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    donation_amount = models.DecimalField(max_digits=10, decimal_places=2)
    donation_date = models.DateField()
    donation_type = models.CharField(max_length=100, choices=[('Cash', 'Cash'), ('Goods', 'Goods'), ('Sponsorship', 'Sponsorship')])
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.full_name