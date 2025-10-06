# -*- coding: utf-8 -*-
"""
Created on Sun Oct  5 11:33:58 2025

@author: Subin-PC
"""

def generate_schedule(principal, annual_rate, payments):
    monthly_rate = annual_rate / 12
    balance = principal
    total_interest = 0

    print("\nRepayment Schedule:")
    print(f"{'Month':<6}{'Opening Balance':<18}{'Interest':<10}{'Payment':<10}{'Closing Balance':<18}")
    print("-" * 65)

    for month, payment in enumerate(payments, start=1):
        opening_balance = balance
        interest = round(opening_balance * monthly_rate, 2)
        total_due = opening_balance + interest
        total_interest += interest

        if payment >= total_due:
            actual_payment = total_due
            closing_balance = 0
        else:
            actual_payment = payment
            closing_balance = round(total_due - payment, 2)

        print(f"{month:<6}{opening_balance:<18.2f}{interest:<10.2f}{actual_payment:<10.2f}{closing_balance:<18.2f}")

        balance = closing_balance
        if balance <= 0:
            break

    print("\nTotal Interest Paid:", round(total_interest, 2))


if __name__ == "__main__":
    # Input from user
    principal = float(input("Enter principal loan amount: "))
    annual_rate = float(input("Enter annual interest rate (in %): ")) / 100
    n = int(input("Enter number of months you plan to keep the loan: "))

    case = input("Choose repayment type - Same (S), Different (D), or No payments until end (N): ").strip().upper()

    payments = []

    if case == "S":
        amt = float(input("Enter the monthly payment amount: "))
        payments = [amt] * n
        generate_schedule(principal, annual_rate, payments)

    elif case == "D":
        for i in range(n):
            payment = float(input(f"Enter payment for month {i+1}: "))
            payments.append(payment)
        generate_schedule(principal, annual_rate, payments)

    elif case == "N":
        # Simple interest, one-time repayment
        total_interest = round(principal * annual_rate * (n/12), 2)
        total_due = principal + total_interest
        print(f"\nNo payments made for {n} months.")
        print(f"Total Interest Due: {total_interest}")
        print(f"Total Amount Payable at the end: {total_due}")
