from django.db import models

import shortuuid

def shorten_name(name):
    if len(name) <= 3:
        return name.lower()
    else:
        return name[0].lower() + ''.join([ch for ch in name[1:].lower() if ch not in 'aeiouy'][:2])


def generate_uuid(prefix=''):
    assert len(prefix) == 3, 'Prefix must be 3 characters long for Short UUID'
    return (prefix + '_' if prefix else '') + shortuuid.uuid()


class ShortPrefixedIdModel(models.Model):

    id = models.CharField(primary_key=True, max_length=26, editable=False)

    @classmethod
    def create_id(cls):
        return generate_uuid(prefix=getattr(cls, 'ID_PREFIX', shorten_name(cls.__name__)))

    def save(self, *args, **kwargs):
        # Provide default value for ID field
        if self._state.adding:
            self.id = self.create_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.id

    class Meta:
        abstract = True
