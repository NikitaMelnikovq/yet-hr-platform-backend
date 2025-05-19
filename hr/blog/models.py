from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название блога')
    date = models.DateField(auto_now_add=True)
    text = models.TextField(verbose_name='Текст блога')
    image = models.ImageField(verbose_name='Изображение', upload_to='images/')