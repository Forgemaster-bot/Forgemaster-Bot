class StopException(Exception):
    """
    Exception used to stop a menu.
    """
    def __init__(self, message=None):
        """
        Exception raised when user wants to go back to previous menu

        :param message: string containing reason for message, None if no special reason
        """
        self.message = message


class ExitException(Exception):
    """
    Exception used to exit the '$menu' command.
    """

    def __init__(self, message=None):
        """
        Exception raised when user wants to exit all menus.
        Message contains special information if not raised due to user input.

        :param message: string containing reason for exit, else None
        """
        self.message = message
