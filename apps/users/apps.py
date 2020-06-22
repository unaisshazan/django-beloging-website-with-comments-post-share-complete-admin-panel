from django.apps import AppConfig

class UsersAppConfig(AppConfig):
    
    name = 'site_repo.apps.users'
    
    def ready(self):
        import signals