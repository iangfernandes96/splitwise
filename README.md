## README

Creating a sample FastAPI application.
This application is a splitwise app, meant to create transactions/bills between people/groups

v0.1:
    1. Ability to create users, groups
    2. Ability to create bills between two or more people
        2.a Assume that only one person pays the bill
    3. Ability to split bills equally
    4. Ability to update bills amount
    5. Ability to view who owes me, who do i owe
    
    * Settling debts will be handled later


Users:
    user_id
    name
    email

Group:
    group_id
    members
    name

Bills:
    bill_id
    bill_name
    bill_amount
    bill_payer
    owed_by [list of all people who owe money to payee]
    group_id [Optional, if passed, assumed bill is split evenly between the group]

Tally:
    txn_id
    payer
    payee
    amount 
    bill_id


