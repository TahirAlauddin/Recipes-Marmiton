from allauth.account.adapter import DefaultAccountAdapter


class CustomUserAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):

        birth_date = request.POST.dict().get('birth_date')

        # Manullay adding birth_date
        user.birth_date = birth_date
        return super(CustomUserAdapter, self).save_user(
            request, user, form, commit
        )