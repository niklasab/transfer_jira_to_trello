import requests
import csv
import time
import argparse

def get_key():
    global key
    return key

def get_token():
    global token
    return token

def list_boards():
    url = f"https://api.trello.com/1/members/me/boards"
    querystring = {"key": get_key(), "token": get_token()}
    response = requests.request("GET", url, params=querystring)
    boards = response.json()

    print("Available boards:")
    for board in boards:
        print(f"    Name: {board['name']} Id: {board['id']}")

def get_cards(board_id):
    url = f"https://api.trello.com/1/boards/{board_id}/cards"
    querystring = {"key": get_key(), "token": get_token()}
    response = requests.request("GET", url, params=querystring)
    board_cards = response
    return board_cards.json()

def list_lists(board_id):
    url = f"https://api.trello.com/1/boards/{board_id}/lists"
    querystring = {"key": get_key(), "token": get_token()}
    response = requests.request("GET", url, params=querystring)
    lists = response.json()
    print("Available lists:")
    for listjson in lists:
        print(f"Name: {listjson['name']} Id: {listjson['id']}")

def create_card(list_id, card_name, desc):
    url = f"https://api.trello.com/1/cards"
    querystring = {"name": card_name, "idList": list_id, "key": get_key(), "token": get_token(), "desc": desc}
    response = requests.request("POST", url, params=querystring)
    card_id = response.json()["id"]
    return card_id

def transfer_jira_csv_to_trello_cards(jira_csv, trello_list_id):
    with open(jira_csv, newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        idx = 0
        for row in csv_reader:
            if idx == 0:
                idx += 1
                continue
            idx += 1
            task_name=f"{row[0]} [{row[1]}][{row[4]}]"
            desc = "IMPORTED FROM JIRA\n\n"
            desc += f"Created: {row[19]}\n"
            desc += f"Updated: {row[20]}\n"
            desc += f"Date3: {row[21]}\n"
            desc += f"Comment: {row[49]}\n"
            desc += f"Description:\n{row[25]}\n"
            create_card(trello_list_id, task_name, desc)
            print(f"Transferred task: {task_name}")
            time.sleep(0.5) # Limit requests per second
        print(f"Transferred {idx} tasks")


def main():
    global key
    global token

    parser = argparse.ArgumentParser(description='Transfer JIRA cards to Trello board',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--key', dest='key')
    parser.add_argument('--token', dest='token')
    parser.add_argument('--jiracsv', dest='jiracsv')
    parser.add_argument('--listboards', action='store_true')
    parser.add_argument('--boardid', dest='boardid')
    parser.add_argument('--listlists', action='store_true')
    parser.add_argument('--listid', dest='listid')
    parser.add_argument('--transfer', action='store_true')
    options = parser.parse_args()

    if options.key and options.token:
        key = options.key
        token = options.token
    else:
        print("Must supply key and secret (see README)")
        return

    if options.listboards:
        list_boards()
        return

    if options.listlists:
        if options.boardid:
            list_lists(options.boardid)
        else:
            print("Must provide board id to list lists")
        return

    if options.transfer:
        if options.jiracsv and options.listid:
            transfer_jira_csv_to_trello_cards(options.jiracsv, options.listid)
        else:
            print("Must supply jiracsv and list id to transfer")
        return

    print("Must supply more arguments")


if __name__ == '__main__':
    main()
