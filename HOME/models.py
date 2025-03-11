from django.db import models



class Client(models.Model):
    client_name = models.CharField(max_length=100)
    client_logo = models.ImageField(name="client_logo",upload_to='media/clients')

    def __str__(self):
        return self.client_name

class Interest(models.Model):
    interest_name = models.CharField(max_length=100)
    interest_icon = models.ImageField(name="interest_icon",upload_to='media/interests')
    
    def __str__(self):
        return self.interest_name