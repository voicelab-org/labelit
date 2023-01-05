from django.apps import AppConfig


class labelitConfig(AppConfig):
    name = "labelit"

    def ready(self):
        # import labelit.signals.validators.annotation_labels_changed
        import labelit.signals.denormalizers.annotation_saved
