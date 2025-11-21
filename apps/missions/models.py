from django.db import models


class Mission(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    cat = models.OneToOneField(
        'spy_cats.Cat',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mission'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def check_completion(self):
        if self.targets.exists() and self.targets.filter(is_completed=False).count() == 0:
            self.is_completed = True
            self.save(update_fields=['is_completed'])
