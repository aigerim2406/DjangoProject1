from django.db import models
from django.urls import reverse


class Aigerim(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(blank=True, verbose_name="Текст поста")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="ФОто")
    price = models.BigIntegerField(default=1000, verbose_name="Цена")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name="Категория")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})

    class Meta:
        verbose_name = 'Известные Пандоры'
        verbose_name_plural = 'Известные Пандоры'
        ordering = ['title']

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name = 'Категория')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']