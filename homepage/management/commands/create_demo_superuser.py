from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Создать/обновить демонстрационного superuser для /admin/."

    def handle(self, *args, **options):
        User = get_user_model()
        user, _ = User.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@example.local"},
        )
        user.is_staff = True
        user.is_superuser = True
        user.set_password("admin123")
        user.save()
        self.stdout.write(self.style.SUCCESS("Django Admin: admin / admin123"))
