# Transfer JIRA cards to Trello board
This repo contains a simple script for moving JIRA cards to Trello.
Note, the cards won't be identical, the Trello cards only retains the
most important information.

# How-to
1. Go to JIRA / Filters / Advanced issue search
    - Adjust filter for the cards you want to export (e.g. Select project)
    - Export all fields to csv (Jira.csv)
2. Follow https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/ to
   create a token and key
3. List boards to get the board id
``` shell
python sync_jira_trello.py --key <INSERT KEY> --token <INSERT TOKEN> --listboards
```
4. List the board's lists to get the list id
``` shell
python sync_jira_trello.py --key <INSERT KEY> --token <INSERT TOKEN> --boardid <BOARD ID from previous step>
```
5. Transfer cards
``` shell
python sync_jira_trello.py --key <INSERT KEY> --token <INSERT TOKEN> --listid <LIST ID from previous step> --transfer --jiracsv <EXPORTED CSV from first step>
```


