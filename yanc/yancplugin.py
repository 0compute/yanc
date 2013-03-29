from nose.plugins import Plugin

from yanc.colorstream import ColorStream


class YancPlugin(Plugin):
    """Yet another nose colorer"""

    name = "yanc"

    _options = (
        ("color", "YANC color override - one of on,off [%s]", "store"),
    )

    def options(self, parser, env):
        super(YancPlugin, self).options(parser, env)
        for name, help, action in self._options:
            env_opt = "NOSE_YANC_%s" % name.upper()
            parser.add_option("--yanc-%s" % name.replace("_", "-"),
                              action=action,
                              dest="yanc_%s" % name,
                              default=env.get(env_opt),
                              help=help % env_opt)

    def configure(self, options, conf):
        super(YancPlugin, self).configure(options, conf)
        for name, help, dummy in self._options:
            name = "yanc_%s" % name
            setattr(self, name, getattr(options, name))
        self.color = self.yanc_color != "off" \
            and (self.yanc_color == "on"
                 or (hasattr(self.conf, "stream")
                     and hasattr(self.conf.stream, "isatty")
                     and self.conf.stream.isatty()))

    def begin(self):
        if self.color:
            self.conf.stream = ColorStream(self.conf.stream)

    def finalize(self, result):
        if self.color:
            self.conf.stream = self.conf.stream._stream