#function to handle the profile pictures uploaded by users/customers in their account settings page.
def handle_uploaded_file(f):  
    with open('CRM1/static/images/customer_profile_pic'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)  