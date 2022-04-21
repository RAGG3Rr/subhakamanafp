
from aboutus.models import Contact

def check_contacts(request):
    contacts=Contact.objects.all()
    return {'contacts': contacts}