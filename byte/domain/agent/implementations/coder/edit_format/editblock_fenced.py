from byte.domain.agent.implementations.coder.edit_format.base import (
    EditFormat,
    EditFormatPrompts,
)

# Credits to: https://github.com/Aider-AI/aider/blob/e4fc2f515d9ed76b14b79a4b02740cf54d5a0c0b/aider/coders/editblock_fenced_prompts.py
edit_format_system = """
# *SEARCH/REPLACE block* Rules:

Every *SEARCH/REPLACE block* must use this format:
1. The opening fence and code language, eg: {fence_open}python
2. The *FULL* file path alone on a line, verbatim. No bold asterisks, no quotes around it, no escaping of characters, etc.
3. The start of search block: <<<<<<< SEARCH
4. A contiguous chunk of lines to search for in the existing source code
5. The dividing line: =======
6. The lines to replace into the source code
7. The end of the replace block: >>>>>>> REPLACE
8. The closing fence: {fence_close}

Use the *FULL* file path, as shown to you by the user.

Every *SEARCH* section must *EXACTLY MATCH* the existing file content, character for character, including all comments, docstrings, etc.
If the file contains code or other data wrapped/escaped in json/xml/quotes or other containers, you need to propose edits to the literal contents of the file, including the container markup.

*SEARCH/REPLACE* blocks will *only* replace the first match occurrence.
Including multiple unique *SEARCH/REPLACE* blocks if needed.
Include enough lines in each SEARCH section to uniquely match each set of lines that need to change.

Keep *SEARCH/REPLACE* blocks concise.
Break large *SEARCH/REPLACE* blocks into a series of smaller blocks that each change a small portion of the file.
Include just the changing lines, and a few surrounding lines if needed for uniqueness.
Do not include long runs of unchanging lines in *SEARCH/REPLACE* blocks.

Only create *SEARCH/REPLACE* blocks for files that the user has added to the chat!

To move code within a file, use 2 *SEARCH/REPLACE* blocks: 1 to delete it from its current location, 1 to insert it in the new location.

Pay attention to which filenames the user wants you to edit, especially if they are asking you to create a new file.

If you want to put code in a new file, use a *SEARCH/REPLACE block* with:
- A new file path, including dir name if needed
- An empty `SEARCH` section
- The new file's contents in the `REPLACE` section

To rename files which have been added to the chat, use shell commands at the end of your response.

If the user just says something like "ok" or "go ahead" or "do that" they probably want you to make SEARCH/REPLACE blocks for the code changes you just proposed.
The user will say when they've applied your edits. If they haven't explicitly confirmed the edits have been applied, they probably want proper SEARCH/REPLACE blocks.

ONLY EVER RETURN CODE IN A *SEARCH/REPLACE BLOCK*!
"""

# {quad_backtick_reminder}

example_messages = [
    (
        "user",
        "Change get_factorial() to use math.factorial",
    ),
    (
        "assistant",
        """To make this change we need to modify `mathweb/flask/app.py` to:

1. Import the math package.
2. Remove the existing factorial() function.
3. Update get_factorial() to call math.factorial instead.

Here are the *SEARCH/REPLACE* blocks:

{fence_open}python
mathweb/flask/app.py
<<<<<<< SEARCH
from flask import Flask
=======
import math
from flask import Flask
>>>>>>> REPLACE
{fence_close}

{fence_open}python
mathweb/flask/app.py
<<<<<<< SEARCH
def factorial(n):
    "compute factorial"

    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

=======
>>>>>>> REPLACE
{fence_close}

{fence_open}python
mathweb/flask/app.py
<<<<<<< SEARCH
    return str(factorial(n))
=======
    return str(math.factorial(n))
>>>>>>> REPLACE
{fence_close}
<<<<<<< HEAD
""",
    ),
    (
        "user",
        "Refactor hello() into its own file.",
    ),
    (
        "assistant",
        """To make this change we need to modify `main.py` and make a new file `hello.py`:

1. Make a new hello.py file with hello() in it.
2. Remove hello() from main.py and replace it with an import.

Here are the *SEARCH/REPLACE* blocks:

{fence_open}python
hello.py
<<<<<<< SEARCH
=======
def hello():
    "print a greeting"

    print("hello")
>>>>>>> REPLACE
{fence_close}

{fence_open}python
main.py
<<<<<<< SEARCH
def hello():
    "print a greeting"

    print("hello")
=======
from hello import hello
>>>>>>> REPLACE
{fence_close}
""",
    ),
]


class BlockedFenceEditFormat(EditFormat):
    def __init__(self):
        self.prompts = EditFormatPrompts(
            system=edit_format_system, examples=example_messages
        )
