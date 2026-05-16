from django.db import models
from django.utils import timezone
import secrets
import hashlib
import base64


class BaseModel(models.Model):
    """
    Abstract Base Model - Adds security fields to ANY table
    Does NOT include primary key - each table defines its own ID field
    """

    # ========== SECURITY FIELDS (Not primary keys!) ==========
    salt = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Cryptographic salt for this record"
    )

    nonce = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Cryptographic nonce (number used once)"
    )

    tag = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Security tag for verification"
    )

    record_hash = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        db_index=True,
        help_text="SHA-3 hash for tamper detection (NOT an ID field)"
    )

    # ========== AUDIT FIELDS ==========
    created_by = models.ForeignKey(
        'AppUser.User',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_created",
        help_text="User who created this record"
    )

    created_on = models.DateTimeField(
        default=timezone.now,
        blank=True,
        null=True,
        help_text="When this record was created"
    )

    updated_by = models.ForeignKey(
        'AppUser.User',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_updated",
        help_text="User who last updated this record"
    )

    updated_on = models.DateTimeField(
        default=timezone.now,
        blank=True,
        null=True,
        help_text="When this record was last updated"
    )

    # ========== EXTRA FIELDS ==========
    version = models.PositiveIntegerField(
        default=1,
        help_text="Record version number (increments on each update)"
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Soft delete flag"
    )

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        help_text="IP address of creator"
    )

    class Meta:
        abstract = True  # No database table created
        indexes = [
            models.Index(fields=['record_hash']),  # Index for verification queries
            models.Index(fields=['is_active']),
            models.Index(fields=['created_on']),
            models.Index(fields=['updated_on']),
        ]

    def save(self, *args, **kwargs):
        """Auto-generate security fields on creation/update"""
        is_new = self.pk is None  # pk is the model's own ID field
        # is_new = True  # pk is the model's own ID field

        if is_new:
            # Generate security fields only on creation
            self.salt = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8')
            self.nonce = base64.urlsafe_b64encode(secrets.token_bytes(64)).decode('utf-8')
            self.tag = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8')

        # Always update hash on every save
        self.record_hash = self._generate_hash()

        # Update timestamp and version
        self.updated_on = timezone.now()
        if not is_new:
            self.version += 1

        super().save(*args, **kwargs)

    def _generate_hash(self):
        """Generate SHA3-512 hash for integrity checking"""
        # # Collect all field values EXCEPT security fields
        # field_values = []
        # for field in self._meta.fields:
        #     # Skip security and audit fields for hash calculation
        #     if field.name not in ['salt', 'nonce', 'tag', 'record_hash',
        #                           'created_on', 'updated_on', 'created_by',
        #                           'updated_by', 'ip_address']:
        #         value = getattr(self, field.name)
        #         if value is None:
        #             field_values.append('None')
        #         elif hasattr(value, 'pk'):  # ForeignKey
        #             field_values.append(str(value.pk))
        #         elif hasattr(value, 'strftime'):  # DateTime
        #             field_values.append(value.isoformat())
        #         else:
        #             field_values.append(str(value))

        # Combine: salt:nonce:tag:field1:field2:...
        # data_string = f"{self.salt}:{self.nonce}:{self.tag}:{':'.join(field_values)}"
        data_string = f"{self.salt}:{self.nonce}:{self.tag}"

        # Return SHA3-512 hash (128 hex characters)
        return hashlib.sha3_512(data_string.encode('utf-8')).hexdigest()

    def verify_integrity(self):
        """Verify record hasn't been tampered with"""
        if not self.record_hash:
            return True
        current_hash = self._generate_hash()
        is_valid = current_hash == self.record_hash

        if not is_valid:
            print(f"⚠️ INTEGRITY FAILED: {self.__class__.__name__} ID: {self.pk}")

        return is_valid

    def soft_delete(self):
        """Soft delete this record"""
        self.is_active = False
        self.save()