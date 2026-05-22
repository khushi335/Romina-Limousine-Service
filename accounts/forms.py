from django import forms
# from .models import ProfileData

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model=ProfileData
#         fields=['profile_picture','bio','dob']

#         widgets={
#             'dob':forms.DateInput(attrs={'type':'date'})
#         }

# class ProfileForm(forms.ModelForm):
#     remove_picture = forms.BooleanField(required=False, label='Remove profile picture')

#     class Meta:
#         model = ProfileData
#         fields = ['profile_picture','bio','dob']

#         widgets={
#             'dob':forms.DateInput(attrs={'type':'date'})
#         }

#     def save(self, commit=True):
#         profile = super().save(commit=False)
#         if self.cleaned_data.get('remove_picture') and profile.profile_picture:
#             profile.profile_picture.delete(save=False)
#             profile.profile_picture = None
#         if commit:
#             profile.save()
#         return profile