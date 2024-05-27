from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Record
import os
from django.template.defaultfilters import date
from django.contrib import messages
from django.utils import timezone  # Import timezone module
from django.shortcuts import redirect
def send_mail(request, pk):
    # Retrieve the record object
    record = get_object_or_404(Record, pk=pk)

    # Retrieve the user's email address
    user_email = request.user.email
    task_id = date(record.creation_date, "YmdHis")

    # Generate the file path for the attachment
    file_path = f'D:\\file_generated\\{task_id}.csv'

    # Check if the file exists
    if os.path.exists(file_path):
        try:
            # Create EmailMessage object
            email = EmailMessage(
                subject='Top Secret File',
                body='Please find the attachment in this email.',
                from_email=settings.EMAIL_HOST_USER,
                to=[user_email],
            )

            # Attach the file to the email
            with open(file_path, 'rb') as file:
                email.attach(f'{task_id}.csv', file.read(), 'text/csv')

            # Send the email
            email.send()

            # Update record status to "Email Sent"
            record.status = 'Email Sent'

            # Update end time after sending the email
            record.end_time = timezone.now()
            
            record.save()

            # Return a success response
            messages.success(request, "Email sent successfully.")
            return redirect("dashboard")
        except Exception as e:
            # Handle any exceptions that occur during email sending
            messages.error(request, f"Error sending email: {str(e)}")
            return HttpResponse("Error sending email.", status=500)
    else:
        # Return a failure response if the file does not exist
        messages.error(request, "Attachment not found.")
        return HttpResponse("Attachment not found.", status=404)
