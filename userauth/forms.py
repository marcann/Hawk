from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from userauth.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges with the given email and password.
    """

    def __unicode__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        del self.fields['username']

    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    """
    A form for updating users. Includes all fields on the user, replaces
    the password field with the admin's password hash display field.
    """

    def __unicode__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        del self.fields['username']

        class Meta:
            model = CustomUser
