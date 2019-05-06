from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'
    verbose_name = 'وبلاگ'

    def ready(self):
        import blog.signals

