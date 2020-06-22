import datetime
from django.contrib.auth.models import User
from site_repo.apps.expenses.models import Expense
from site_repo.apps.users.API import register_user

_expense_fields = (
                  'month_balanced',
                  'year_balanced',
                  'expense_sum',
                  'expense_divorcee_participate',
                  'desc',
                  'place_of_purchase',
                  'notes')

def add_users(Lusers,send_email=False):
    """ [{'username':'user1','password':'123'}, ... ] """
    
    for Duser in Lusers:
        Duser['mail'] = send_email
        register_user(**Duser)

        
def add_expenses(Dexpenses):
    """ Dexpenses is a dict with username and list of tuples,each with the expense fields values
    {'use1':[(1,2016,100,50,'desc','place','notes'),(...)],'user2':[...]}
    """
    t = datetime.datetime.today()
    for username,Lexpenses in Dexpenses.iteritems():
        owner = User.objects.get(username=username)
        for expense_tuple in Lexpenses:
            Dexpense = {x[0]:x[1] for x in zip(_expense_fields,expense_tuple)}
            Dexpense['owner'] = owner
            Dexpense['date_purchased'] = t
            e = Expense(**Dexpense)
            e.save()


   