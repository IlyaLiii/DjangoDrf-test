from django.contrib.auth.models import User

try:
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
except Exception:
    print("Superuser has already been created")
