from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save


class User(AbstractUser):
    is_director = models.BooleanField(
        default=True,
    )
    is_agent = models.BooleanField(
        default=False,
    )


class UserPortfolio(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Портфолио пользователя"
        verbose_name_plural = "Портфолио пользователя"


class Lead(models.Model):
    first_name = models.CharField(max_length=20, verbose_name="Имя")
    last_name = models.CharField(max_length=25, verbose_name="Фамилия")
    age = models.IntegerField(default=0, verbose_name="Возраст")
    company = models.ForeignKey(UserPortfolio, on_delete=models.CASCADE)
    agent = models.ForeignKey(
        "Agent", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Агент"
    )
    category = models.ForeignKey(
        "Category",
        related_name="leads",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
    )
    review = models.TextField(verbose_name="Описание")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    number = models.CharField(max_length=19, verbose_name="Номер телефона")
    email = models.EmailField(verbose_name="Почта")
    converted_date = models.DateTimeField(
        null=True, blank=True, verbose_name="Дата обращения"
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Лиды"
        verbose_name_plural = "Лиды"


class Agent(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    company = models.ForeignKey(
        UserPortfolio,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.user.username} / {self.user.email}"

    class Meta:
        verbose_name = "Агенты"
        verbose_name_plural = "Агенты"


class Category(models.Model):
    name = models.CharField(max_length=40)
    company = models.ForeignKey(UserPortfolio, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категории"
        verbose_name_plural = "Категории"


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserPortfolio.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User)
