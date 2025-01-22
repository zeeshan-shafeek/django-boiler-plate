import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class BaseModel(models.Model):
    """
    Abstract base model with common fields for UUID, timestamps, and display ID.
    """
    standard_fields = ["id", "display_id", "created_at", "updated_at"]

    # Auto-generated timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, db_index=True, verbose_name=_("updated at"))

    # Unique identifier and a short display version
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, verbose_name=_("id"))
    display_id = models.CharField(max_length=6, editable=False, default="------", verbose_name=_("display id"))

    def get_changes(self):
        """
        Return field changes between the latest and previous records (requires Django Simple History).
        """
        new_record = self.history.first()
        old_record = new_record.prev_record

        if old_record is None:
            return None

        # Build a dictionary of changes
        return {
            change.field: {"old": change.old, "new": change.new}
            for change in new_record.diff_against(old_record).changes
        }

    def save(self, *args, **kwargs):
        """
        Ensure UUID and display ID are generated before saving.
        """
        if self.id is None:
            self.id = uuid.uuid4().hex
        self.display_id = str(self.id)[:6].upper()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ["-created_at"]  # Sort by creation date (newest first)

    def __str__(self):
        return self.display_id


class Auditable(models.Model):
    """
    Abstract model to track record creation and updates by users.
    """
    standard_fields = ["created_by", "updated_by"]

    # References to the user who created/updated the record
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, related_name="created%(app_label)s_%(class)s_related", on_delete=models.SET_NULL
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, related_name="updated%(app_label)s_%(class)s_related", on_delete=models.SET_NULL
    )

    class Meta:
        abstract = True


class ActiveManager(models.Manager):
    """
    Custom manager for handling active/inactive records.
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)  # Only active records

    def delete(self):
        self.get_queryset().update(is_active=False)  # Soft delete

    def undelete(self):
        self.get_queryset().update(is_active=True)  # Restore soft-deleted records

    def hard_delete(self):
        super().delete()  # Permanently delete


class Activable(models.Model):
    """
    Abstract model for soft-deletable records.
    """
    standard_fields = ["is_active"]

    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_("is active"))

    # Default and custom managers
    admin_objects = models.Manager()
    objects = ActiveManager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        """
        Mark record as inactive (soft delete).
        """
        self.is_active = False
        self.save()

    def undelete(self, *args, **kwargs):
        """
        Restore a soft-deleted record.
        """
        self.is_active = True
        self.save()

    def hard_delete(self, *args, **kwargs):
        """
        Permanently delete the record.
        """
        super().delete(*args, **kwargs)

    def was_soft_deleted(self):
        """
        Check if the record was previously active but is now inactive.
        """
        new_record = self.history.first()
        old_record = new_record.prev_record

        return old_record and old_record.is_active and not self.is_active
