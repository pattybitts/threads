class ValidCommands:
    basic_commands = [
        "add_char",
        "edit_char",
        "disp_char"
        ]

    @staticmethod
    def is_valid(cmd):
        print(cmd)
        print(ValidCommands.basic_commands)
        return cmd in ValidCommands.basic_commands

    @staticmethod
    def disp_char(input):
        return "goob"