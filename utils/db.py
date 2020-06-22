from django.db import connections


def run_sql(sql,*args):
    
    try:
        connection = connections['default']
        cursor = connection.cursor()
        cursor.execute(sql,args)
        connection.commit()
    except:
        try:
            raise
        finally:
            connection.rollback()
    else:
        return cursor.fetchall()
    
