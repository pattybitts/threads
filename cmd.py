class ValidCommands:
    basic_commands = [
        "add_char",
        "edit_char",
        "disp_char",
        "gen_archive"
        ]

    @staticmethod
    def is_valid(cmd):
        return cmd in ValidCommands.basic_commands