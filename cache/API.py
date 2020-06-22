from django.core.cache import cache

   
def get_user_cache(user):
    
    D = cache.get("user_%s"%user.id)
    return {} if D == None else D
    

def set_user_cache(user,Dvals):
    
    D = get_user_cache(user)
    for key,value in Dvals.items():
        D[key] = value
    cache.set("user_%s"%user.id,D)
    
def clear_user_cache(user):
    
    cache.delete("user_%s"%user.id)
    