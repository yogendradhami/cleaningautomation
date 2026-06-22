from django.db import models

class Enquiry(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=50, blank=True)
    property_type = models.CharField(max_length=100, blank=True)
    suburb = models.CharField(max_length=200, blank=True)
    preferred_date = models.DateField(null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} <{self.email}> ({self.created_at:%Y-%m-%d %H:%M})"


class EnquiryImage(models.Model):
    enquiry = models.ForeignKey(Enquiry, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='enquiries/%Y/%m/%d')

    def __str__(self):
        return f"Image for {self.enquiry.name} ({self.id})"
