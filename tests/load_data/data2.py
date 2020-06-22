import datetime
t = datetime.datetime.today()
crr_month,crr_year = t.month,t.year

Lusers = []
Dexpenses = {}

# Expenses list for multiple expenses tests
# The full expense tuple is (1,2016,$100,50%,'desc','place','notes')
expenses = [
    (160,50,'School books','Books store',''),
    (90,50,'Sneakers','Amazon',''),
    (300,50,'Soccer League','Soccer League',''),
    (240,50,'Scouts','Scouts',''),
    (30,50,'Snacks and drinks for the school event','Whole Foods','mid-year party'),
    (80,50,'Coat','Target',''),
    (150,50,'Math tutor','Elaine',''),
    (150,50,'School payment','School','half year payment'),
    (75,50,'Shoes','Zappos',''),
    (28,50,'Disney Toys','Disney','Elsa, Baz'),
    (20,50,"A gift for friend's birthday",'Gifts shop',''),
    (32,50,'Coloring set','Crayola','for the holiday'),
    (80,50,'Dress for the school party','Dress store',''),
    (350,50,'Smart phone','Amazon',''),
]