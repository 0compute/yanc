import re


class ColorStream(object):

    COLOR_NAMES = ["grey", "red", "green", "yellow", "blue", "magenta", "cyan",
                   "white"]
    COLOR_CODES = dict(zip(COLOR_NAMES, list(range(30, 38))))
    COLOR_FMT = "\033[%dm%s\033[0m"

    COLORS = dict(
        green=("OK", "ok", "."),
        red=("ERROR", "FAILED", "errors", "E"),
        yellow=("FAILURE", "FAIL", "failures", "F"),
        magenta=("SKIP", "S"),
        blue=("-" * 70, "=" * 70),
    )

    def __init__(self, stream):
        self._stream = stream
        self._color_map = {}
        self._patten_map = {}
        for color, labels in self.COLORS.items():
            for label in labels:
                self._color_map[label] = color
                if len(label) > 1:
                    self._patten_map[label] = re.compile("%s=\d+" % label)

    def __getattr__(self, key):
        return getattr(self._stream, key)

    def _color_wrap(self, string, color):
        return self.COLOR_FMT % (self.COLOR_CODES[color], string)

    def _colorize(self, string, color=None):
        if string:
            if color is None:
                color = self._color_map.get(string)
                if color is None:
                    for key in self._color_map:
                        # looking for a test failure as LABEL: str(test)
                        if string.startswith(key + ":"):
                            segments = string.split(":")
                            label = self._colorize(segments[0] + ":",
                                                   self._color_map[key])
                            desc = ":".join(segments[1:])
                            if desc.startswith(" Failure: "):
                                desc = self._color_wrap(desc,
                                                        self._color_map[key])
                            return label + desc
                    for key, key_color in self._color_map.items():
                        # looking for label=number in the summary
                        pattern = self._patten_map.get(key)
                        if pattern is not None:
                            for match in pattern.findall(string):
                                string = string.replace(
                                    match, self._colorize(match, key_color)
                                )
            if color is not None:
                string = self._color_wrap(string, color)
        return string

    def write(self, string):
        self._stream.write(self._colorize(string))

    def writeln(self, string=""):
        self._stream.writeln(self._colorize(string))