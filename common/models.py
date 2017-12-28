from django.db import models

from .utils import unique_id, get_object_or_none


class BaseModel(models.Model):
    """Base model"""

    id = models.CharField(max_length=22, editable=False, primary_key=True)

    def __make_id(self):
        uid = unique_id()[::2]
        obj = get_object_or_none(self.__class__, pk=uid)

        self.id = uid if not obj else ''

    def save(self, *args, **kwargs):
        while not self.id: self.__make_id()
        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class EmailLog(BaseModel):

    email = models.CharField(max_length=200, null=False,blank=False)
    name = models.CharField(max_length=200, null=False,blank=False)
    lastName = models.CharField(max_length=200, null=False,blank=False)
    created = models.DateTimeField(auto_now_add=True)    

    class Meta:
        verbose_name = "Registro de mailing"
        verbose_name_plural = "Registros de mailing"