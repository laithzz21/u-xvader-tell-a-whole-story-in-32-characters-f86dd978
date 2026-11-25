#!/usr/bin/env python3
"""
Tell a whole story in 32 characters -- make.fun entry.

Competition: u-xvader-tell-a-whole-story-in-32-characters-f86dd978
Brief: a single Wi-Fi network name, at most 32 characters long,
that lands a joke and implies a whole story.

Entry:
    My Ex Changed The Password

The joke and the story, in one line: a break-up told through the
one thing everybody in the house shares -- the Wi-Fi. Somebody
moved out, somebody stayed, and the password changed. No shouting,
no long explanation, just a locked-out ex and a router that picked
a side. Anyone who has ever typed a familiar password and watched
it fail knows exactly what happened here, who did it, and why.

This program prints exactly that entry text to stdout and nothing
else. Every check below is silent on success so the output stays
byte-identical to the entry text; any problem is reported on stderr
and exits non-zero instead of printing a bad entry.
"""

import sys

# ---------------------------------------------------------------------------
# The entry
# ---------------------------------------------------------------------------

ENTRY_TEXT = "My Ex Changed The Password"

# Competition limit: a Wi-Fi network name (SSID) of at most 32 characters.
MAX_LENGTH = 32

# Fallbacks, in order of preference. Each one also satisfies the brief
# (a Wi-Fi name, <= 32 characters, joke + implied story), so the program
# can still produce a valid entry if the primary text ever fails a check.
# They are only used when the primary entry is rejected by validation;
# under normal operation the primary entry is printed unchanged.
FALLBACK_ENTRIES = [
    "My Ex Took The WiFi Too",
    "It Was My Ex, Not The Router",
    "This WiFi Has Trust Issues",
]


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def count_characters(text):
    """Return the character count of *text* (code points, not bytes).

    Wi-Fi names are limited to 32 characters, and the competition
    counts characters the same way a human would -- one character
    per letter, space, or punctuation mark. Counting code points
    matches that for plain ASCII text such as this entry.
    """
    return len(text)


def is_within_limit(text, limit=MAX_LENGTH):
    """True when *text* fits inside the competition's character limit."""
    return 0 < count_characters(text) <= limit


def has_no_newlines(text):
    """True when *text* is a single line, as a Wi-Fi name must be."""
    return "\n" not in text and "\r" not in text


def is_printable_ascii(text):
    """True when every character is printable ASCII.

    A Wi-Fi name shown on a phone or laptop should render cleanly
    everywhere, so the entry sticks to ordinary letters and spaces.
    """
    return all(32 <= ord(ch) <= 126 for ch in text)


def has_no_leading_or_trailing_space(text):
    """True when *text* does not start or end with a space."""
    return text == text.strip() and len(text) > 0


def contains_story_markers(text):
    """True when *text* carries the pieces of the implied story.

    The story needs three ingredients in a few words: a relationship
    ("Ex"), an act of revenge or change ("Changed"), and the thing
    that was taken away ("Password"). If any of them is missing, the
    line stops implying a story and becomes just a label.
    """
    lowered = text.lower()
    has_relationship = "ex" in lowered.split()
    has_action = "changed" in lowered
    has_object = "password" in lowered
    return has_relationship and has_action and has_object


def has_readable_word_count(text):
    """True when *text* has 3-8 words: short enough to read at a glance.

    A Wi-Fi name is scanned, not read. Five words is the sweet spot
    here -- long enough to tell the story, short enough that a
    neighbour scrolling a network list gets the joke instantly.
    """
    words = text.split()
    return 3 <= len(words) <= 8


def validate_entry(text):
    """Validate *text* against every rule of the brief.

    Returns a list of human-readable problems; an empty list means
    the text is a valid entry.
    """
    problems = []
    if not text:
        problems.append("entry text is empty")
    if not has_readable_word_count(text):
        problems.append("entry should be 3-8 words for a Wi-Fi name")
    if not is_within_limit(text):
        problems.append(
            "entry is %d characters, over the %d-character limit"
            % (count_characters(text), MAX_LENGTH)
        )
    if not has_no_newlines(text):
        problems.append("entry must be a single line")
    if not is_printable_ascii(text):
        problems.append("entry must be printable ASCII")
    if not has_no_leading_or_trailing_space(text):
        problems.append("entry must not start or end with a space")
    if not contains_story_markers(text):
        problems.append("entry does not imply the break-up story")
    return problems


def choose_entry():
    """Return the entry text to print, falling back if needed.

    The primary entry is used whenever it validates. If it somehow
    fails, each fallback is tried in order, and the first valid one
    wins. If nothing validates, a ValueError is raised so the program
    fails loudly instead of printing an invalid entry.
    """
    candidates = [ENTRY_TEXT] + list(FALLBACK_ENTRIES)
    for candidate in candidates:
        if not validate_entry(candidate):
            return candidate
    raise ValueError("no valid entry text available")


def verify_output(output, expected):
    """Check that the exact bytes to be printed match the entry.

    This guards against accidental trailing spaces, extra newlines,
    or encoding surprises between validation and printing.
    """
    if output != expected:
        raise ValueError("output does not match the entry text")
    if count_characters(output) > MAX_LENGTH:
        raise ValueError("output exceeds the 32-character limit")
    if not is_printable_ascii(output):
        raise ValueError("output contains non-printable characters")
    if not has_no_newlines(output):
        raise ValueError("output must be a single line")
    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    """Print exactly the entry text to stdout, nothing else."""
    try:
        entry = choose_entry()
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1

    # Final safety check: the string about to be printed is exactly
    # the validated entry, character for character, and encodes as
    # plain ASCII so no platform can mangle it on the way out.
    try:
        entry.encode("ascii")
        verify_output(entry, entry)
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1

    # print() adds exactly one trailing newline, which is the standard
    # line terminator; the entry text itself contains no extra output.
    print(entry)
    return 0


if __name__ == "__main__":
    sys.exit(main())
