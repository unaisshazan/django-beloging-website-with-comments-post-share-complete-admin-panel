from django.conf import settings

sql = """SELECT id FROM {db_name}.search_searchitems
WHERE object_account_id = %s AND MATCH(object_name,search_text)
AGAINST (%s IN BOOLEAN MODE)
LIMIT %s
""".format(db_name=settings.DATABASES['default']['NAME'])

D = {
'MIN_LENGTH_SEARCH_QUERY':4,
'WILDCARD':'*',
'AUTO_WILDCARD':True,
'MAX_ENTRIES':100,
'SELECT': sql
}

if hasattr(settings,"SEARCH_SETTINGS"):
    for key,value in getattr(settings,"SEARCH_SETTINGS").iteritems:
        D[key] = value
        
MIN_LENGTH_SEARCH_QUERY = D['MIN_LENGTH_SEARCH_QUERY']
WILDCARD = D['WILDCARD']
AUTO_WILDCARD = D['AUTO_WILDCARD']
MAX_ENTRIES = D['MAX_ENTRIES']
SELECT = D['SELECT']
        

        
