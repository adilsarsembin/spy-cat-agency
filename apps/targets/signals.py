from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import Target


@receiver(pre_delete, sender=Target)
def validate_target_deletion(sender, instance, **kwargs):
    mission = instance.mission
    remaining_targets = mission.targets.exclude(pk=instance.pk).count()
    if remaining_targets < 1:
        raise ValidationError("Cannot delete target. A mission must have at least 1 target.")
