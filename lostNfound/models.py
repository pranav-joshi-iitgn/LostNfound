from django.db import models
from django.utils import timezone

# Create your models here.

class Person(models.Model):
    username = models.CharField(max_length=100,default="")
    name = models.CharField(max_length=100,default="unknown")
    password = models.CharField(max_length=100,default="X")
    contact = models.CharField(max_length=100,default="unknown")
    email = models.CharField(max_length=1000,default="unknown")
    image = models.TextField(max_length=1000,default="default.png")
    address = models.TextField(max_length=500,default="unknown")
    def __repr__(self):
        return self.username

class Item(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE,default="")
    name = models.CharField(max_length=50)
    date = models.DateField(default=timezone.now)
    keywords = models.CharField(max_length=100,default="")
    description = models.TextField(default="")
    image = models.TextField(max_length=1000,default="default.png")
    location = models.CharField(max_length=1000, default="")
    def __repr__(self):
        return self.name
    def unlink(self,claim_id,password):
        if self.person.password != password:
            return "wrong password"
        try:
            c = self.claim_set.get(pk=claim_id)
        except:
            return "this claim isn't for the item"
        try:
            self.claim_set.remove(c)
            self.save()
            return "done"
        except:
            return "error"
    def dissolve(self,password):
        if self.person.password != password:
            return "wrong password"
        try:
            for c in self.claim_set.all():
                c.items.remove(self)
                c.save()
            self.delete()
            return "done"
        except:
            return "error"

class Claim(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE,default="")
    items = models.ManyToManyField(Item)
    name = models.CharField(max_length=50,default="unknown")
    date = models.DateField(default = timezone.now)
    keywords = models.CharField(max_length=100,default="")
    description = models.TextField(default="")
    image = models.TextField(max_length=1000,default="default.png")
    location = models.CharField(max_length=1000, default="")
    def __repr__(self):
        return self.name
    def unlink(self,item_id,password):
        if self.person.password != password:
            return "wrong password"
        try:
            i = self.items.get(pk=item_id)
        except:
            return "this claim isn't for the item"
        try:
            self.items.remove(i)
            self.save()
            return "done"
        except:
            return "error"
    def dissolve(self,password):
        if self.person.password != password:
            return "wrong password"
        try:
            for i in self.items.all():
                i.claim_set.remove(self)
                i.save()
            self.delete()
            return "done"
        except:
            return "error"

class Report(models.Model):
    criminal = models.ForeignKey(Person, on_delete=models.CASCADE,default="",related_name="crimes")
    reportee = models.ForeignKey(Person, on_delete=models.CASCADE,default="",related_name="reports")
    description = models.TextField(max_length=1000,default="")
    date = models.DateTimeField(default = timezone.now)
    def __repr__(self):
        return self.reportee.name + " reported " + self.criminal.name + " on " + str(self.date)