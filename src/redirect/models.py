from django.db import models
from django.contrib.auth.models import User

    
class ShortLink(models.Model):
    class Meta:
        ordering = ['-created_at']
    
    code = models.CharField(max_length=24, primary_key=True)
    url = models.URLField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    @staticmethod    
    def get_shortlink(code):
        return ShortLink.objects.filter(code=code).first()

    @staticmethod    
    def get_shortlinks_of(user):
        return ShortLink.objects.filter(owner=user)
    
    @staticmethod    
    def get_all_shortlinks():
        return ShortLink.objects.all()
    
    