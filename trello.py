import requests
import sys

auth_params = {
    'key': "cb24af4cd83ed36d5e7b509f5f11ace4",
    'token': "efcb7f49c7dad7cf02ab48cdc52a9f54d3b75bb650b2687d0bdfdab00d275042",
}

base_url = "https://api.trello.com/1/{}"
board_id = "1WFKY645"



def read():
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for column in column_data:
        print(column['name'])
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        if not task_data:
            print('\t' + 'No Tasks!')
            continue
        for task in task_data:
            print('\t' + task['name'])


def create(name, column_name):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for column in column_data:
        if column['name'] == column_name:
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            break


def move(name, column_name):
    column_data = requests.get(base_url.format('boards') + '/' + board_id +'/lists', params=auth_params).json()
    task_id = None
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                task_id = task['id']
                break
        if task_id:
            break

    for column in column_data:
        if column['name'] == column_name:
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})

print(sys.argv[0])

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])