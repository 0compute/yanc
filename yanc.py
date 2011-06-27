from nose.plugins import Plugin

import termstyle

    
class ColorStreamProxy(object):

    _color_map = {
        "OK" : "green",
        "ok" : "green",
        "." : "green",
        "FAILED" : "red",
        "ERROR" : "red",
        "E" : "red",
        "FAILURE" : "yellow",
        "F" : "yellow",
        "SKIP" : "magenta",
        "S" : "magenta",
        "-" * 70 : "blue",
        "=" * 70 : "blue",
        }
    
    def __init__(self, stream):
        self._stream = stream
        
    def __getattr__(self, key):
        return getattr(self._stream, key)
    
    def _colorize(self, string, color=None):
        if string:
            if color is None:
                color = self._color_map.get(string)
            if color is None:
                for key in self._color_map:
                    if string.startswith(key + ":"):
                        parts = string.split(":")
                        return self._colorize(parts[0] + ":", self._color_map[key]) + ":".join(parts[1:])
            else:
                string = getattr(termstyle, color)(string)
        return string
    
    def write(self, string):
        self._stream.write(self._colorize(string))
    
    def writeln(self, string=""):
        self._stream.writeln(self._colorize(string))

    
class YANC(Plugin):
    """Yet another nose colorer"""
    
    name = "yanc"
    
    _options = (
        ("color", "YANC color override - one of on,off [%s]", "store"),
        )
    
    def options(self, parser, env):
        super(YANC, self).options(parser, env)
        for name, help, action in self._options:
            env_opt = "NOSE_YANC_%s" % name.upper()
            parser.add_option("--yanc-%s" % name.replace("_", "-"),
                              action=action,
                              dest="yanc_%s" % name,
                              default=env.get(env_opt),
                              help=help % env_opt)
        
    
    def configure(self, options, conf):
        super(YANC, self).configure(options, conf)
        for name, help, dummy in self._options:
            name = "yanc_%s" % name
            setattr(self, name, getattr(options, name))
        self.color = self.yanc_color !="off" \
                         and (self.yanc_color == "on" \
                             or (hasattr(self.conf.stream, "isatty") \
                                 and self.conf.stream.isatty()))
        
    def begin(self):
        if self.color:
            self.conf.stream = ColorStreamProxy(self.conf.stream)
    
    def finalize(self, result):
        if self.color:
            self.conf.stream = self.conf.stream._stream
    