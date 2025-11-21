from django.db import models
from django.core.exceptions import ValidationError


class Note(models.Model):
    target = models.ForeignKey(
        'targets.Target',
        on_delete=models.CASCADE,
        related_name='note_entries'
    )
    cat = models.ForeignKey(
        'spy_cats.Cat',
        on_delete=models.CASCADE,
        related_name='notes'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Note by {self.cat.name} on {self.target.name}"

    def clean(self):
        if self.pk:
            original = Note.objects.get(pk=self.pk)
            if original.target.is_completed:
                raise ValidationError(
                    "Cannot update notes for a completed target. Notes are frozen once target is completed."
                )

    def save(self, *args, **kwargs):
        if self.pk:
            original = Note.objects.get(pk=self.pk)
            if original.target.is_completed:
                raise ValidationError(
                    "Cannot update notes for a completed target. Notes are frozen once target is completed."
                )
        self.full_clean()
        super().save(*args, **kwargs)
