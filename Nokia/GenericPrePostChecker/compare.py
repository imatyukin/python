from colorama import init
from CommandParser.command_parser import CommandParser
from compare_dicts.compare_dicts import CompareDicts
init()


class Color:
    """Object just to color strings in terminal output."""
    OK = '\033[32m'
    WARN = '\033[33m'
    FAIL = '\033[31m'
    CHANGE = '\033[34m'
    END = '\033[0m'


def print_results(command, results):
    border = '+' + '-' * 11 + '+' + '-' * 65 + '+'
    print(border)
    padding = int((65 - len(command)) / 2)
    modulo = (65 - len(command)) % 2
    print('|  Command  |{}{}{}{}|'.format(' ' * padding, command, ' ' * padding, ' ' * modulo))
    print(border)
    if results:
        if any(results.values()):  # at least one list contains elements
            for msg in results['missing']:
                print('|{} - MISSING{} | {}{}|'.format(Color.FAIL, Color.END, msg, ' ' * (64 - len(msg))))
                print(border)
            for msg in results['new']:
                print('|{} + NEW{}     | {}{}|'.format(Color.WARN, Color.END, msg, ' ' * (64 - len(msg))))
                print(border)
            for msg in results['changed']:
                print('|{} ~ CHANGED{} | {}{}|'.format(Color.CHANGE, Color.END, msg, ' ' * (64 - len(msg))))
                print(border)
        else:
            print('|    {}OK{}     | Verification successful{}|'.format(Color.OK, Color.END, ' ' * 41))
            print(border)
    else:
        print('|  {}UNKNOWN{}  | No results to print{}|'.format(Color.WARN, Color.END, ' ' * 45))
        print(border)


def main(pre_file_name, post_file_name):

    with open(pre_file_name) as pre_file:
        pre_output = pre_file.read()

    with open(post_file_name) as post_file:
        post_output = post_file.read()

    CommandParser.template_collection = '..\..\TextFSM_templates'
    print('Parsing pre-check ....')
    pre_dict = CommandParser(pre_output).get_all_command_output_structured(output="dict")
    print('Parsed commands: {}'.format('\n'.join(pre_dict.keys())))
    print('Parsing post-check ....')
    post_dict = CommandParser(post_output).get_all_command_output_structured(output="dict")
    print('Parsed commands: {}'.format('\n'.join(pre_dict.keys())))

    for command, pre_content in pre_dict.items():
        post_content = post_dict.get(command, {})
        results = CompareDicts(pre_content, post_content).get_results()
        print_results(command, results)

    from pprint import pprint
    pprint(pre_dict.get('show router pim group'))
    pprint(post_dict.get('show router pim group'))


if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(prog='python3 compare.py', description='Compare router pre/post checks.')
    parser.add_argument('pre', help='Input file with pre-check.')
    parser.add_argument('post', help='Input file with post-check')
    args = parser.parse_args()

    main(args.pre, args.post)
