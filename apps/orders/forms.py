from django import forms
from ..accounts.models import Address
class AddressSelectionForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(AddressSelectionForm, self).__init__(*args, **kwargs)
        addresses = Address.objects.filter(user=user)
        choices = [(address.id, address.complete_address) for address in addresses]
        self.fields['address'] = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)