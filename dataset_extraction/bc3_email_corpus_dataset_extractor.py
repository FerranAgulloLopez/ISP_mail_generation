import argparse
import json
import xml.etree.ElementTree as xml


def parse_arguments():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--data_directory',  type=str, help="Path to data directory", required=True)
    parser.add_argument('--output_directory', type=str, help="Path to output directory to where store the output files", required=True)
    return parser.parse_args()


def save_json(path: str, data: dict):
    path += '.json'
    with open(path, 'w') as file:
        json.dump(data, file, indent=2)


def main(data_directory: str, output_directory: str):
    # load corpus and annotation files
    corpus_path = data_directory + '/corpus.xml'
    annotation_path = data_directory + '/annotation.xml'
    corpus_data = xml.parse(corpus_path).getroot()
    annotation_data = xml.parse(annotation_path).getroot()

    # extract important information to a dict
    mails = []
    for thread in corpus_data:
        # extract information from thread
        thread_id = thread.find('listno').text
        thread_annotations = annotation_data.find('./*[listno=\'' + thread_id + '\']')
        for mail in thread.iter('DOC'):
            # extract information from mail
            mail_subject = mail.find('Subject').text
            mail_content = ''
            extractive_summary = ''
            for sentence in mail.find('Text'):
                mail_content += sentence.text

                # extract annotation information
                sentence_id = sentence.attrib['id']
                extractive_annotations = thread_annotations.findall('./annotation/sentences/*[@id=\'' + sentence_id + '\']')
                if len(extractive_annotations) > 1:  # we do a majority vote between the annotators
                    extractive_summary += sentence.text

            # create mail dict
            mail = {
                'subject': mail_subject,
                'content': mail_content,
                'extractive_summary': extractive_summary
            }
            mails.append(mail)

    # write dict as a json file in output directory
    output = {
        'mails': mails
    }
    save_json(output_directory + '/extracted_bc3_email_corpus_dataset', output)


if __name__ == '__main__':
    # Get input params (data directory)
    args = parse_arguments()

    # Run main program
    main(args.data_directory, args.output_directory)
