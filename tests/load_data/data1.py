import datetime
t = datetime.datetime.today()
crr_month,crr_year = t.month,t.year

Lusers = [{'username':'john','password':'123456','email':'john@example.com','account_code':''}]
          
#(1,2016,$100,50%,'desc','place','notes')
Dexpenses = {'john':[
    (crr_month,crr_year,130,50,'School','Book Store',''),
     (crr_month,crr_year,90,50,'Sneakers','Amazon',''),
]}