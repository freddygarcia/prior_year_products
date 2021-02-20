from models import IRSFinder

# to beatify the dict output
import json
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('action',  type=str, help='Download taxes pdf files', choices=['download', 'json'])
parser.add_argument('--form_names', '-f', type=str, nargs='+', help='Form name (when action=download) / Form names (when action=json)', required=True)
parser.add_argument('--year-from', '-yf',  type=int, help='Year from ( when action=download )')
parser.add_argument('--year-to', '-yt',  type=int, help='Year to ( when action=download )')

args = parser.parse_args()

finder = IRSFinder()

form_names = args.form_names

if args.action == 'download':

    if not (args.year_from and args.year_to):
        parser.print_help()
        exit()

    form_name = form_names[0]
    year_range = (args.year_from, args.year_to)
    finder.download_taxes(form_name, *year_range)

elif args.action == 'json':
    json_dict = finder.get_taxes_json(form_names)
    json = json.dumps(json_dict, indent=4)
    
    print(json)

    with open('json', 'w') as f:
        f.write(json)
