import json
import os

if __name__ == '__main__':
    # file_amount = len(os.listdir('./content'))
    # print(file_amount)
    # print(type(os.listdir('./content')))
    # file_list = os.listdir('./content')
    # file_list.sort()

    with open('../data/threads/dataset.json', 'r') as f:
        dataset = json.load(f)
    current_thread = []
    current_thread_id = dataset[0]['id'].split('-')[1]

    for i, _ in enumerate(dataset):
        if i % 1000 == 0:
            print('{}/{}'.format(i, len(dataset)))

        email_content = dataset[i]
        # # Read text file
        # try:
        #     with open(os.path.join('./content', filename), 'r') as f:
        #         email_content = json.load(f)
        # except UnicodeDecodeError:
        #     continue

        thread = dataset[i]['id'].split('-')[1]
        if current_thread_id != thread:
            with open('threads/thread_{}.json'.format(current_thread_id), 'w') as f:
                json.dump(current_thread, f)
            current_thread = []
            current_thread_id = thread

        current_thread.append(email_content)

    with open('threads/thread_{}.json'.format(current_thread_id), 'w') as f:
        json.dump(current_thread, f)

    print('Created {} JSON files'.format(len(os.listdir('../data/threads'))))
