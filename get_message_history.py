import requests
from argparse import ArgumentParser
import json

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--token', required=True)
    parser.add_argument('--isbot', default=False)
    parser.add_argument('--channelid', required=True)
    parser.add_argument('--limit', default=None, type=int)
    parser.add_argument('--output', required=True)
    return parser.parse_args()

def get_message_history(token, channel_id, before):
    api_url = "https://discord.com/api/"
    headers = dict(Authorization=token)
    params = dict(limit=100)
    if before is not None:
        params['before'] = before
    r = requests.get("%s/channels/%s/messages" % (api_url, channel_id), headers=headers, params=params)
    return r.json()

def main(args):
    # prep token for user or bot
    token = ('Bot %s' % args.token) if args.isbot else args.token

    # send requests to api
    messages = []
    before = None

    while True:
        # get message history
        history = get_message_history(token, args.channelid, before)

        # if no new messages, break 
        if len(history) == 0:
            break

        # update message array
        messages += history

        # if required limit reached
        if args.limit is not None and len(messages) >= args.limit:
            break

        # update before var for next call
        before = messages[-1]['id']
    
    # write to output file
    with open(args.output, 'w') as f:
        json.dump(messages, f, indent=4)


if __name__ == '__main__':
    args = parse_args()
    main(args)
