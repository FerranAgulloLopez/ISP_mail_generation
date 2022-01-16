import json
import re
import os

if __name__ == '__main__':
    pattern1 = re.compile('[a-z]+=\\".*?\\".*?\\n')
    pattern2 = re.compile('[A-Za-z]+:.*?\\n+')

    file_amount = len(os.listdir('./w3c-emails'))
    for i, filename in enumerate(os.listdir('./w3c-emails')):
        if i % 1000 == 0:
            print('{}/{}'.format(i, file_amount))

        # Read text file
        try:
            with open(os.path.join('./w3c-emails', filename), 'r') as f:
                entire_email = f.readlines()
        except UnicodeDecodeError:
            continue

        # Remove header
        while entire_email and pattern1.match(entire_email[0]) is not None:
            del entire_email[0]
        while entire_email and entire_email[0] == '\n':
            del entire_email[0]
        while entire_email and pattern2.match(entire_email[0]) is not None:
            del entire_email[0]
        while entire_email and entire_email[0] == '\n':
            del entire_email[0]

        # Join the lines of the email body
        entire_email = ''.join(entire_email)

        # Dump email content into JSON
        filename_no_ext, _ = os.path.splitext(filename)
        with open('content/' + filename_no_ext + '.json', 'w') as f:
            json.dump({'content': entire_email}, f)

    print('Extracted {} emails'.format(len(os.listdir('./content'))))
