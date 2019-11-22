class CleanConfig:
    def __init__(self, config):
        self.default_config = config

    def _clean(self, name, settings):
        if name.lower() != "default":
            to_delete = list(key for key, value in settings.items() if not value)
            for item in to_delete:
                del settings[item]
        return {name: settings}

    @property
    def cleaned(self):
        clean_config = self.default_config
        for name, settings in tuple(self.default_config["databases"].items()):
            clean_config["databases"].update(self._clean(name, settings))
        return clean_config
