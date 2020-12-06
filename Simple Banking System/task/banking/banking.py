# Write your code here
import random
import sqlite3
from random import randint

global card_num, pin_number, card_balance, deposit, card_number_input, card_number_entered

conn = sqlite3.connect('card.s3db')
cursor = conn.cursor()


class SimpleBankingSystem:
    def __init__(self):
        self.PIN = str(randint(1000, 9999))
        self.card_balance = 0
        self.start_text = """1. Create an account
2. Log into account
0. Exit"""
        self.balance_menu = """
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
"""

    def start_menu(self):
        print(self.start_text)

    def luhn_algo(self):
        global card_num
        major_bank_id = 400000

        # start luhn algorithm
        card_no = [int(i) for i in str(major_bank_id)]
        card_num = [int(i) for i in str(major_bank_id)]
        cust_acc_no = random.sample(range(9), 9)
        for i in cust_acc_no:
            card_no.append(i)
            card_num.append(i)
        for t in range(0, 15, 2):
            card_no[t] = card_no[t] * 2
        for i in range(len(card_no)):
            if card_no[i] > 9:
                card_no[i] -= 9
        s = sum(card_no)
        mod = s % 10
        check_sum = 0 if mod == 0 else (10 - mod)
        card_num.append(check_sum)
        card_num = [str(i) for i in card_num]
        card_num = ''.join(card_num)
        return int(card_num)

    def in_menu_luhn_algo(self, card_number):
        # global card_number_input
        card_number_input = list(card_number.strip())
        # Remove the last digit from the card number
        check_digit = card_number_input.pop()
        # Reverse the order of the remaining numbers
        card_number_input.reverse()
        processed_digits = []
        for index, digit in enumerate(card_number_input):
            if index % 2 == 0:
                doubled_digit = int(digit) * 2
                # Subtract 9 from any results that are greater than 9
                if doubled_digit > 9:
                    doubled_digit = doubled_digit - 9
                processed_digits.append(doubled_digit)
            else:
                processed_digits.append(int(digit))
        total = int(check_digit) + sum(processed_digits)
        # Verify that the sum of the digits is divisible by 10
        if total % 10 == 0:
            return True
        else:
            return False

    def pin_generator(self):
        global pin_number
        pin_number = str(randint(1000, 9999))
        return pin_number

    def the_balance(self):
        global card_balance
        card_balance = self.card_balance
        return self.the_balance()

    def create_table(self):
        cursor.execute('''CREATE TABLE IF NOT EXISTS card
        (id INTEGER primary key autoincrement, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);''')
        conn.commit()
        # self.insert_data()

    def insert_data(self):
        global card_num, pin_number, card_balance
        cursor.execute(f'''insert into card (number, pin, balance) 
            values ({card_num}, {pin_number}, {self.card_balance})''')
        conn.commit()

    def main_menu(self):
        global card_num
        self.create_table()
        self.start_menu()
        while True:
            cursor.execute('SELECT * FROM card')
            table = cursor.fetchall()
            user_input = input()
            if user_input == '1':
                print("\nYour card has been created\nYour card number:")
                print(self.luhn_algo())
                print('Your card PIN:')
                print(f'{self.pin_generator()}\n')
                # print(table)
                self.insert_data()
                self.start_menu()
            elif user_input == '2':
                print('\nEnter your card number:')
                card_number_entered = input()
                print('Enter your PIN:')
                pin_entered = input()
                # if card_num == card_number_entered and pin_number == pin_entered:
                for row in table:
                    if card_number_entered in row and pin_entered in row:
                        print('\nYou have successfully logged in!')
                        print(self.balance_menu)
                        choice = input()
                        while True:
                            # return table
                            if choice == '1':
                                # print(table)
                                print(f'\nBalance: {self.card_balance}')
                                print(self.balance_menu)
                                choice = input()
                            elif choice == '2':
                                deposit = int(input('Enter income:\n'))
                                self.card_balance += deposit
                                cursor.execute(
                                    f'''update card set balance = balance + {deposit} where number = {card_number_entered}''')
                                conn.commit()
                                print("Income was added!")
                                # print(table)
                                print(self.balance_menu)
                                choice = input()
                            elif choice == '3':
                                # print(table)
                                card_number_input = input('Transfer\nEnter card number:\n')
                                if self.in_menu_luhn_algo(card_number_input):
                                    for row in table:
                                        if card_number_input in row:
                                            deposit = int(input('Enter how much money you want to transfer:\n'))
                                            if self.card_balance < deposit:
                                                print("Not enough money!")
                                                break
                                            else:
                                                cursor.execute(
                                                    f'''update card set balance = balance + {deposit} where number = {card_number_input}''')
                                                conn.commit()
                                                self.card_balance -= deposit
                                                cursor.execute(
                                                    f'''update card set balance = balance - {deposit} where number = {card_number_entered}''')
                                                conn.commit()
                                                print('Success!')
                                                break
                                        if card_number_input == card_number_entered:
                                            print("You can't transfer money to the same account!")
                                            break
                                    else:
                                        print("Such a card does not exist.")
                                    # print(table)
                                    print(self.balance_menu)
                                    choice = input()
                                else:
                                    print('Probably you made a mistake in the card number. Please try again!')
                                    print(self.balance_menu)
                                    choice = input()
                            elif choice == '4':
                                cursor.execute(f'''delete from card where number = {card_number_entered}''')
                                conn.commit()
                                card_num = None
                                cursor.execute('SELECT * FROM card')
                                table = cursor.fetchall()
                                # print(table)
                                print('The account has been closed!')
                                self.start_menu()
                                break
                            elif choice == '5':
                                print('\nYou have successfully logged out!\n')
                                self.start_menu()
                                break
                            elif choice == '0':
                                exit('\nBye!')
                    else:
                        print('\nWrong card number or PIN!\n')
                        # print('Probably you made a mistake in the card number. Please try again!')
                        self.start_menu()
            elif user_input == '0':
                exit('\nBye!')
            else:
                print()
                self.start_menu()
                # user_input = input()


if __name__ == "__main__":
    SimpleBankingSystem().main_menu()


