# class Account:
#     def __init__(self,acc_no, acc_bal):
#         print("Account created")
#         self.acc_no = acc_no
#         self.acc_bal = acc_bal
#         self.get_acc_bal()


#     def debit(self,amount):
#         print(f"account debited by Rs.{amount} ")
#         self.acc_bal -= amount
#         self.get_acc_bal()


#     def credit(self,amount):
#         print(f"account credited by Rs.{amount} ")
#         self.get_acc_bal()

#     def get_acc_bal(self):
#         print(f"Account balance: {self.acc_bal}")

    

# a1 = Account(1,1000)
# # a1.get_acc_bal()
# a1.debit(200)
# # a1.get_acc_bal()
# a1.credit(210)
# # a1.get_acc_bal()

from app.utils.extra import test

test()