import os

users = []
budget_history = []
original_budget = {}
current_budget = {}
user_hosts = {}


def get_initial_data():
    global users, budget_history, original_budget, current_budget

    if not users:
        if not os.path.exists('budget_history.csv'):
            print("ERROR: Set budget_history.csv first with users and their original budgets")
            exit(0)

        with open('budget_history.csv') as csv_file:
            file_rows = [l.strip().split(',') for l in csv_file.readlines()]
            users = file_rows[0]
            budget_history = [[float(column) for column in row] for row in file_rows[1:]]
            original_budget = {users[i]: budget_history[0][i] for i in range(len(users))}
            current_budget = {users[i]: budget_history[-1][i] for i in range(len(users))}

    return (users, budget_history, original_budget, current_budget)


def get_user_hosts():
    global user_hosts

    if not user_hosts:
        if not os.path.exists('user_hosts.csv'):
            print("WARNING: users need to register their hosts using /등록/<username>")
        else:
            with open('user_hosts.csv') as csv_file:
                file_rows = [l.strip().split(',') for l in csv_file.readlines()]
                user_hosts = {file_rows[0][i]: file_rows[1][i] for i in range(len(file_rows[0]))}

    return user_hosts
