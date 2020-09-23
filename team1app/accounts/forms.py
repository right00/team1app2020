
from .models import  User
from django.contrib.auth.forms import UserCreationForm
class SignUpForm(UserCreationForm):
    """ユーザー登録用フォーム"""

    class Meta:
   
        model = User
        fields = ('username', 'email', 'password1', 'password2')