from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Friend(models.Model):
    name = models.CharField(max_length=100)
    mail = models.EmailField(max_length=200)
    gender = models.BooleanField()
    age = models.IntegerField(validators=[ \
        MinValueValidator(0), \
        MaxValueValidator(150)])
    birthday = models.DateField()

    def __str__(self):
        return '<Friend:id=' + str(self.id) + ', ' + \
        self.name + '(' + str(self.age) + ')>'
    
class Hoge(models.Model):
    name=models.CharField(max_length=100)

class Message(models.Model):
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE,related_name="message")
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=300)
    pub_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '<Message:id=' + str(self.id) + ', ' + \
        self.title + '(' + str(self.pub_date) + ')>'
    
    # class Meta:
    #     ordering = ('-pub_date',)