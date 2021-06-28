from django.db import models, transaction


class Archivable(object):
    # This is only for mypy's benefit, it is overridden by all classes that inherit from Archivable
    # e.g. see Template.__mro__
    # It gets rid of over 30 errors
    is_active = models.BooleanField()

    def archive(self):
        self.is_active = False
        self.save()  # type: ignore[attr-defined]

    # TODO: we have to expand this unarchive, sometimes it should be blocked.
    # e.g. the system shouldn't allow you to have more than one active
    # translation for language X for some template (see what was done in
    # ICMSLST-483)
    def unarchive(self):
        self.is_active = True
        self.save()  # type: ignore[attr-defined]


class Sortable(object):
    @transaction.atomic
    def swap_order(self, swap_with):
        current_order = self.order  # type: ignore[has-type]
        new_order = swap_with.order
        self.order = new_order
        swap_with.order = current_order
        self.save()  # type: ignore[attr-defined]
        swap_with.save()
