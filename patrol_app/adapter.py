from allauth.account.adapter import DefaultAccountAdapter

class AccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        """
        これは、allauth登録を通じてユーザーを保存する際に呼び出されます。
        ユーザーオブジェクトに追加データを設定するために、これをオーバーライドします。
        """
        # まだユーザーを永続化しないので、commit=Falseを渡します
      
        user = super(AccountAdapter, self).save_user(request, user, form, commit=False)
        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        user.email = form.cleaned_data.get('email')
        user.telephone_number = form.cleaned_data.get('telephone_number')
        user.post_code = form.cleaned_data.get('post_code')
        user.address = form.cleaned_data.get('address')
        user.save()