## About
A simple Python script to easily hide and make visible files or directories on Windows and Linux.

## How it works
### On Linux:
* It adds a dot at the beginning of a file or directory (target) to hide it.
* It removes the dot from the beginning of the target to make it visible.

### On Windows:
* It changes target's properties (to hidden) by running "attrib +H" to hide.
* It changes target's properties by running "attrib -H" to make visible.

## More
It doesn't do anything special at a low level.
After hiding the targets, they can still be easily seen by just toggling an option in the file explorer.

Requires Python 3.10+, because of the match-case statement (but it can be changed to if-elif-else statement).
