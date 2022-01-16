import json
import re
import os


def extract_content(plain_text_email, get_subject=False):
    pattern1 = re.compile('[a-z]+=\\".*?\\".*?\\n')
    pattern2 = re.compile('[A-Za-z]+:.*?\\n+')

    email_content = {}

    # Remove header
    while plain_text_email:
        m = pattern1.match(plain_text_email[0])
        if m is None:
            break
        if m.string[:7] == 'subject' and get_subject:
            email_content['subject'] = m.string[9:-3]
        del plain_text_email[0]
    while plain_text_email and plain_text_email[0] == '\n':
        del plain_text_email[0]
    while plain_text_email and pattern2.match(plain_text_email[0]) is not None:
        del plain_text_email[0]
    while plain_text_email and plain_text_email[0] == '\n':
        del plain_text_email[0]

    # Join the lines of the email body
    email_content['content'] = ''.join(plain_text_email)
    return email_content


def is_attachment_mail(email_content):
    pattern_list = [
        re.compile('[ \n?-]*\* text\/html attachment: stored[ \n]*'),
        re.compile('[ \n?-]*\* text\/html attachment: stored[ \n]+\* text\/html attachment: [a-zA-Z0-9._-]+[ \n]*'),
        re.compile('[ \n?-]*\* text\/html attachment: stored[ \n]+\* application\/octet-stream attachment: [a-zA-Z0-9._-]+[ \n]*'),
        re.compile('[ \n?-]*application/octet-stream attachment: [a-zA-Z0-9._-]+[ \n]*'),
        re.compile('[ \n?-]*\* TEXT\/PLAIN charset=US-ASCII attachment: stored[ \n]*'),
        re.compile('[ \n?-]*text\/plain, charset=\\\"iso-8859-1\\\" attachment: stored[ \n]*'),
        re.compile('[ \n?-]*\(\'binary\' encoding is not supported, stored as-is\)[ \n?-]*tex\t/html attachment: stored[ \n]*'),
        re.compile('This is a multipart message in MIME format\n>\n>--_NextPart_000_.*')
    ]
    other_string_list = [
        '',
        '    2004??6??16????7??28????????????????????www.rhexpo.com??????\"????100\"??????????????\n    ????????????????????????\n\n\n\n\napplication/octet-stream attachment: ________.doc\n\napplication/octet-stream attachment: ________.doc\n\n\n\n\n',
        'text/html attachment: aile oxeye sixgun\n\n\n\n\n'
    ]
    return any(regex.match(email_content) for regex in pattern_list) or email_content in other_string_list


if __name__ == '__main__':

    file_list = os.listdir('./w3c-emails')
    file_list.sort()
    file_amount = len(os.listdir('./w3c-emails'))
    print(f'Preprocessing {file_amount} emails')

    dataset = []

    successfully_preprocessed_emails = 0
    attachment_emails = 0
    for i, filename in enumerate(file_list):
        if i % 1000 == 0:
            print(f'{i}/{file_amount}')

        # Read text file
        try:
            with open(os.path.join('./w3c-emails', filename), 'r') as f:
                entire_email = f.readlines()
        except UnicodeDecodeError:
            continue

        # Preprocess email
        email_content = extract_content(entire_email, get_subject=True)
        if is_attachment_mail(email_content['content']):
            attachment_emails += 1
            continue
        successfully_preprocessed_emails += 1

        # Add to current thread
        email_content['id'] = os.path.splitext(filename)[0]
        dataset.append(email_content)

    with open(f'../data/threads/dataset.json', 'w') as f:
        json.dump(dataset, f)

    print(f'Filtered {attachment_emails} attachment emails')
    print(f'Successfully preprocessed {successfully_preprocessed_emails} emails')
    print(f'Created {len(os.listdir("../data/threads"))} JSON files')
