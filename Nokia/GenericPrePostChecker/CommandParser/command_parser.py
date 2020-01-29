import os
import re
import logging
import textfsm


class CommandParser:
    """Parser for operations on router show command outputs."""
    # path to textFSM template collection dir
    template_collection = "textFSM_templates"

    # Definition of prompt regular expression to detect vendor/os for dynamic template mapping.
    vendor_prompt_re = {
        # regex for prompt       Mapping: vendor, os
        r'\*?[AB]:\S+[#$]': ("nokia", "sros"),
        r'\w+\/\d+\/\w+\/\w+:\S+[#$]': ("cisco", "xr"),
        r'\S+@\S+[>#]': ("juniper", "junos"),
    }

    def __init__(self, input_text: str):
        """Constructor

        Args:
            input_text: Input text-block with show commands output.
        """
        self.input_text = input_text
        self.prompt = self._detect_prompt(input_text)
        self.prompt_re = re.escape(self.prompt)  # escape all special char in prompt, for further regex constructs
        self._detect_vendor()
        self.all_commands = self.find_all_commands()
        self.structured_failed = []

    @staticmethod
    def _detect_prompt(input_text: str) -> str:
        """Find the prompt by the largest number of appearances."""
        prompt_re = r'^\*?(\S+[#>])\s*/*show\s+\S+.*?[\r\n]+'
        prompt_dict = {}
        potential_prompts = re.findall(prompt_re, input_text, re.M | re.S)
        for prompt in potential_prompts:
            if prompt not in prompt_dict:
                prompt_dict[prompt] = 1
            else:
                prompt_dict[prompt] += 1
        occur = 0
        prompt = ""
        for k, v in prompt_dict.items():
            if occur < v:
                prompt = k
            occur = max(occur, v)
        return prompt

    def _detect_vendor(self) -> None:
        """Check detected prompt vs. pre-defined prompt regular expressions to detect vendor/os."""
        for prompt_regex, vendor in self.vendor_prompt_re.items():
            re_obj = re.match(r'{}'.format(prompt_regex), self.prompt)
            if re_obj:
                self.vendor = vendor[0]
                self.ios = vendor[1]
                break
            else:
                self.vendor = "cisco"
                self.ios = "ios"

    def get_command_output(self, command: str) -> str:
        """Gets command output.

        Args:
            command: cli show command ie. 'show version'.

        Returns:
            Text block with command output.
        """
        cmd_escaped = re.escape(command)  # builds re, replace all special characters in command string
        command_re = re.compile(
            r'{0}\s*/*{1}\s*[\r\n]+(.*?)\*?(?={0}|\Z)'.format(self.prompt_re, cmd_escaped),
            re.M | re.S)
        command_outputs = command_re.findall(self.input_text)
        if command_outputs and all(command_outputs):
            output = str(max(command_outputs, key=len))  # when command output is found more than once pick longest one
            return output  # => returns longest command output as string block
        else:
            logging.warning('"{}" command output not found.'.format(command))
            output = ''
            return output

    def find_all_commands(self) -> list:
        """Finds all command names in textual router output.

        Return:
            List with command names as elements.
        """
        command_name_re = r'{}\s*/*((?:show|tools).*?)\s*[\r\n]+'.format(self.prompt_re)
        all_cmnds = re.findall(command_name_re, self.input_text, re.M | re.S)
        all_commands = [cmd.strip() for cmd in all_cmnds]
        return all_commands

    def get_all_command_output(self) -> dict:
        """Finds all command names & outputs in textual router output.

        Returns:
            Dict key = command name val = command output.
            i.e. {'show clock': '18:42:41.321 PST Sun May 12 2019'}
        """
        dict_ = {}
        for command_ in self.all_commands:
            command_output_raw = self.get_command_output(command_)
            if command_output_raw:
                dict_[command_] = command_output_raw
        return dict_

    @staticmethod
    def _clitable_to_list(template: str, command_output: str) -> list:
        """ Transforms TextFSM clitable to list of dicts.

        Args:
            template: TextFSM template file location to parse command.
            command_output: Raw command output.

        Returns:
            List of dicts with textFSM Value name, Value. .
        """
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), template), "r") as template_file:
            fsm = textfsm.TextFSM(template_file)
            fsm_results = fsm.ParseText(command_output)
        list_ = []
        data_validation = {k: None for k in fsm.header}
        for line in fsm_results:
            temp_dict = {}
            for number, value in enumerate(line):
                temp_dict.update({fsm.header[number]: value})
                if value and fsm.header[number] in data_validation:
                    data_validation.pop(fsm.header[number])
            list_.append(temp_dict)
        if data_validation and fsm_results:
            logging.warning('No data found for values: {}. TextFSM template {} might need update.'.format(
                ', '.join(data_validation.keys()), template))
            print(fsm_results)
        return list_

    @staticmethod
    def _clitable_to_dict(template: str, command_output: str) -> dict:
        """ Transforms TextFSM clitable to dict.

        Note:
            TextFSM template value must have Key flag defined with one or more template values.
            When multiple keys used they will be separated with pipe.
            Sometimes combination of two values assures unique keys.

            i.e. Assign interface name as Key template value in show router interfaces as interface names are unique
            in that command output.

        Args:
            template: TextFSM template file location to parse command.
            command_output: Raw command output.

        Returns:
            Dict per Key textFSM template value or dict per Values of only one fsm match in cli table.
        """
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), template), "r") as template_file:
            fsm = textfsm.TextFSM(template_file)
            fsm_results = fsm.ParseText(command_output)
            fsm_keys = fsm.GetValuesByAttrib('Key')

        dict_ = {}
        data_validation = {k: None for k in fsm.header}

        if not fsm_keys:
            if not fsm_results:
                return dict_
            elif len(fsm_results) == 1:  # if only one element in cli table
                for number, value in enumerate(fsm_results[0]):
                    dict_[fsm.header[number]] = value
                    if value and fsm.header[number] in data_validation:
                        data_validation.pop(fsm.header[number])
                if data_validation and fsm_results:
                    logging.warning('No data found for values: {}. TextFSM template {} might need update.'.format(
                        ', '.join(data_validation.keys()), template))
                return dict_
            else:
                raise Exception(
                    textfsm.TextFSMTemplateError(
                        'Multiple fsm_results found but in template:"{}" no value has flag "Key" defined.'.format(
                            template)
                    )
                )
        else:
            key_indexes = []
            for key in fsm_keys:
                key_index = fsm.header.index(key)
                key_indexes.append(key_index)

            for line in fsm_results:
                key_names = []
                for key_index in key_indexes:
                    key_names.append(line[key_index])
                key_name = '|'.join(key_names)
                dict_[key_name] = {}

                for number, value in enumerate(line):
                    if number not in key_indexes:
                        dict_[key_name].update({fsm.header[number]: value})
                    if value and fsm.header[number] in data_validation:
                        data_validation.pop(fsm.header[number])

            if data_validation and fsm_results:
                logging.warning('No data found for values: {}. TextFSM template {} might need update.'.format(
                    ', '.join(data_validation.keys()), template))

            return dict_

    @classmethod
    def cmd_to_dict_by_textfsm(
            cls,
            command_: str,
            command_output: str,
            vendor="nokia",
            ios="sros",
            output="list"
    ) -> dict or list:

        """Takes raw command output and transforms it to dict using textFSM template.
        Dynamically searches for textFSM template based on vendor, os and command name.

        Note:
            Class method, so it can be called externally without object creation.
            Template naming convention must be followed.

        Args:
            command_: Command name ie. 'show version'.
            command_output: Raw command output.
            vendor: Specify vendor name.
            ios: Specify IOS type. This is for template search.
            output:

        Returns:
            Depending on output parameter given

            List of textFSM value names, values
                or
            Dict per textFSM template value with Key flag
        """
        command_full = command_
        if vendor == 'nokia':
            if re.search(r'show router \d+', command_):  # remove service id and use generic router template.
                command_ = re.sub(r'show router \d+', 'show router', command_)
        if re.search(r'\d+\.\d+\.\d+\.\d+/\d+', command_):  # replace subnet with variable name
            command_ = re.sub(r'\d+\.\d+\.\d+\.\d+/\d+', '{{subnet}}', command_)
        elif re.search(r'\d+\.\d+\.\d+\.\d+', command_):  # replace ip with variable name
            command_ = re.sub(r'\d+\.\d+\.\d+\.\d+', '{{ip}}', command_)

        text_fsm_template = "{}{}{}_{}_{}.template".format(
            cls.template_collection, os.path.sep, vendor, ios, command_.replace(" ", "_")
        )
        try:
            if output == "list":
                result = cls._clitable_to_list(text_fsm_template, command_output)
            else:
                result = cls._clitable_to_dict(text_fsm_template, command_output)

            if not result and len(str(command_output).splitlines()) > 1:
                logging.warning('"{}" output found, but template parser did not found anything.'.format(command_full))
                logging.info("Template: {}".format(text_fsm_template))
                logging.info("command output:\n{}".format(command_output))
            return result
        except FileNotFoundError:
            logging.warning(
                'TextFSM template not found for command: "{}".\nExpected template file: "{}"\n'.format(
                    command_full, text_fsm_template
                )
            )
        except textfsm.TextFSMError as e:
            logging.error(
                'TextFSM template file: "{}" returned error: "{}"\n '.format(
                    text_fsm_template, e
                )
            )
        except OSError:
            logging.info(
                'Invalid File name: "{}" \n '.format(
                    text_fsm_template
                )
            )

    def get_command_output_structured(self, command_: str, output="list") -> dict:
        """Method to returned structured command output based on textFSM template.
        Uses textFSM template dynamic mapping.

        Args:
            command_: command name
            output: list or dict

        Returns:
            Dict per first(top) textFSM template value name
                or
            list of textFSM value names, values
                depending on output parameter given.
        """
        raw_command = self.get_command_output(command_)
        result = self.cmd_to_dict_by_textfsm(command_, raw_command, vendor=self.vendor, ios=self.ios, output=output)
        return result

    def get_all_command_output_structured(self, output="list") -> dict:
        """Finds all command names & outputs in textual router output,
         transforms raw outputs to structured by textFSM templates.

        Returns:
            Dict key: command name val: command structured output.
            i.e. {'show clock': [{'Time: '18:42:41', 'Timezone': 'PST', 'Date': 'Sun May 12 2019'}]
        """
        dict_ = {}
        for command_ in self.all_commands:
            command_output_raw = self.get_command_output(command_)
            if command_output_raw:
                command_output_structured = self.cmd_to_dict_by_textfsm(
                    command_,
                    command_output_raw,
                    vendor=self.vendor,
                    ios=self.ios,
                    output=output,
                )
                if command_output_structured:
                    dict_[command_] = command_output_structured
                elif command_output_structured is None:
                    self.structured_failed.append(command_)
        return dict_

    def get_structured_failed_command_output(self) -> dict:
        """Returns all commands which failed to be transformed to by textFSM as text.

        Returns:
            Dict key = command name val = command output.
            i.e. {'show clock': '18:42:41.321 PST Sun May 12 2019'}
        """
        dict_ = {}
        for command_ in self.structured_failed:
            command_output_raw = self.get_command_output(command_)
            if command_output_raw:
                dict_[command_] = command_output_raw
        return dict_


if __name__ == '__main__':
    import sys
    from pprint import pprint
    with open(sys.argv[1], 'r') as f:
        input_text = f.read()
    test_object = CommandParser(input_text)
    sep = '='*120
    # print(sep)
    # print('#'*30, 'RAW TEXT', '#'*30)
    # raw = test_object.get_all_command_output()
    # print(raw)
    # print(sep)
    print(len(test_object.find_all_commands()))
    text = test_object.get_command_output('show router route-table summary')
    struct = test_object.get_command_output_structured('show router isis interface', output="dict")
    # print(test_object.find_all_commands())
    # print(text)
    import yaml
    print(yaml.safe_dump(struct))
    print(len(struct))
