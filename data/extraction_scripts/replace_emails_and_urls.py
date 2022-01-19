import argparse
import json
import re


def parse_arguments():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--path', type=str, help="Path to the JSON file", required=True)

    return parser.parse_args()


def main(args):
    pattern1 = re.compile(
        "(mailto:)?(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    )
    pattern2 = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")

    # summarize bc3
    with open(args.path) as f:
        data = json.load(f)
        mails = data['mails']
        for i, mail in enumerate(mails):
            for k in mails[i]:
                s = mails[i][k]
                s = re.sub(
                    pattern1,
                    '[EMAIL]',
                    s
                )
                s = re.sub(
                    pattern2,
                    '[URL]',
                    s
                )
                mails[i][k] = s
                print(mails[i][k])
                # print()

    with open(args.path, 'w') as file:
        json.dump(data, file, indent=4)


if __name__ == '__main__':
    # parse args
    args = parse_arguments()

    # run main method
    main(args)
