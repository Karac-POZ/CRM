from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class DirectorAndLoginRequiredMixin(AccessMixin):
    """Проверка того, что текущий пользователь аутентифицирован и является директором."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_director:
            return redirect("leads:lead-list")
        return super().dispatch(request, *args, **kwargs)
