from django import forms

class SelectCharacter(forms.Form):
    character = forms.ChoiceField(widget=forms.Select(attrs={'onchange': 'this.form.submit();'}), choices=[])

    def __init__(self, names=None, *args, **kwargs):
        super(SelectCharacter, self).__init__(*args, **kwargs)

        if names:
            self.fields['character'].choices = [(x,x) for x in names]

# class SelectCharacter(forms.Form):
#     def __init__(self, names, *args, **kwargs):
#         options = 
#         super(SelectCharacter, self).__init__(*args, **kwargs)
#         self.fields['names'] = forms.ChoiceField(widget=forms.Select(attrs={'onchange': 'this.form.submit();'}), choices)
    