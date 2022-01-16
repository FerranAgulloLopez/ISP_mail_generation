import json
import argparse
from transformers import T5Tokenizer, T5ForConditionalGeneration


def parse_arguments():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--pretrained-model', type=str, help="Name of the pretrained model", required=True)
    parser.add_argument('--num-beams', type=int, help="Number of beams", required=False, default=3)
    parser.add_argument('--no-repeat-ngram-size', type=int, help="No repeat ngram size", required=False, default=2)
    parser.add_argument('--min-length', type=int, help="Minimum length permitted", required=False, default=5)
    parser.add_argument('--max-length', type=int, help="Maximum length permitted", required=False, default=100)
    parser.add_argument('--repetition-penalty', type=float, help="Repetition penalty", required=False, default=2.0)

    return parser.parse_args()


class Summarizer:

    def __init__(self, pretrained_model: str):
        self.model = T5ForConditionalGeneration.from_pretrained(pretrained_model)
        self.tokenizer = T5Tokenizer.from_pretrained(pretrained_model)

    def summarize(self, text: str, args):
        prepared_text = "summarize: " + text
        tokenized_text = self.tokenizer.encode(prepared_text, return_tensors="pt")

        summary_ids = self.model.generate(tokenized_text,
                                          num_beams=args.num_beams,
                                          no_repeat_ngram_size=args.no_repeat_ngram_size,
                                          min_length=args.min_length,
                                          max_length=args.max_length,
                                          repetition_penalty=args.repetition_penalty)

        return self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)


def extract_text_from_mail(mail: dict):
    subject = mail['subject']
    content = mail['content']
    text = f'{subject}. {content}'
    text = text.strip().replace("\n", "")
    return text


def main(args):
    summarizer = Summarizer(args.pretrained_model)

    # summarize bc3
    with open('data/datasets/extracted/bc3/extracted_bc3_email_corpus_dataset.json') as f:
        data = json.load(f)
        mails = data['mails']
        for index, mail in enumerate(mails):
            print(f'left {len(mails) - index} mails')
            text = extract_text_from_mail(mail)
            mail['abstractive_summary'] = summarizer.summarize(text, args)
            print(mail['abstractive_summary'])
    with open('data/datasets/summarized/bc3/summarized_bc3_email_corpus_dataset.json', 'w') as file:
        json.dump(data, file, indent=4)

    # summarize enron


if __name__ == '__main__':
    # parse args
    args = parse_arguments()

    # run main method
    main(args)
