from BaseGundam import BaseGundam


class GenericGundam(BaseGundam):
    """ A generic Gundam. Meant to be used on any kit that doesn't have any special effects needed.  Such as a Zaku II, Gouf, etc.
    Comes with head, beam saber and 2 weapon leds to be activated by default.
    """
    def __init__(self):
        super().__init__()

    def get_config_file(self) -> str:
        return "config/generic_gundam.json"
