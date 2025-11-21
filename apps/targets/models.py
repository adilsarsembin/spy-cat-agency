from django.db import models
from django.core.exceptions import ValidationError


class Target(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    mission = models.ForeignKey(
        'missions.Mission',
        on_delete=models.CASCADE,
        related_name='targets'
    )
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.name} (Mission: {self.mission.title})"

    def clean(self):
        if self.mission_id:
            target_count = self.mission.targets.exclude(pk=self.pk if self.pk else None).count()
            new_count = target_count + 1
            if new_count < 1:
                raise ValidationError("A mission must have at least 1 target.")
            if new_count > 3:
                raise ValidationError("A mission can have at most 3 targets.")

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                original = Target.objects.get(pk=self.pk)
                if original.is_completed or original.mission.is_completed:
                    update_fields = kwargs.get('update_fields', None)
                    if update_fields is None or 'notes' in update_fields:
                        if self.notes != original.notes:
                            raise ValidationError(
                                "Cannot update notes for a completed target or mission. Notes are frozen once target or mission is completed."
                            )
            except Target.DoesNotExist:
                pass
        self.full_clean()
        super().save(*args, **kwargs)
        if self.is_completed:
            self.mission.check_completion()
