from django.contrib.auth.models import User
from django.conf import settings

class EmailAuth(object):
    
    def get_user(self,user_id):
        
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
                
    def authenticate(self,username,password):
 
        try:
            
            if settings.DEBUG and settings.DEBUG_ALLOW_NON_UNIQUE_EMAIL:
                user = User.objects.filter(email=username).first()
            else:
                user = User.objects.get(email=username)
                
            if user !=None and user.is_active and user.check_password(password):
                return user
            else:
                return None            
                
        except User.DoesNotExist:
            return None
        

            
             
             
        
        
        