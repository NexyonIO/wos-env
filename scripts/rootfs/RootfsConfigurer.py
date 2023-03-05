from scripts.Node import Node
from scripts.Config import Config
import scripts.Utilities as Utilities

import os

OS_RELEASE = {
    "NAME": "\"WaspOS\"",
    "PRETTY_NAME": "\"WaspOS\"",
    "ID": "wos",
    "BUILD_ID": "rolling",
    "ANSI_COLOR": "\"38;2;23;147;209\"",
    "HOME_URL": "\"https://github.com/NexyonIO/\"",
    "DOCUMENTATION_URL": "\"https://github.com/NexyonIO/wiki\"",
    "SUPPORT_URL": "\"https://github.com/NexyonIO/\"",
    "BUG_REPORT_URL": "\"https://github.com/NexyonIO/\"",
    "PRIVACY_POLICY_URL": "\"https://github.com/NexyonIO/\"",
    "LOGO": "wos"
}


class RootfsConfigurer(Node):
    def __init__(self, config, logger, rootfs_image):
        super().__init__("RootfsConfigurer")
        
        self.config: Config = config
        self.rootfs_image = rootfs_image
        self.log = logger.get_from_node(self)

    def configure(self) -> int:
        self.log.info("Configuring rootfs")
        rootfs = self.rootfs_image.tmp_folder.get_path()

        if os.path.isfile(f"{rootfs}/etc/hostname"):
            self.run_command(f"rm {rootfs}/etc/hostname")
        
        self.run_command(f"echo \"{self.config.values['hostname']}\" > {rootfs}/etc/hostname")
        self.run_command(f"rm {rootfs}/etc/os-release")
        for key, item in OS_RELEASE.items():
            self.run_command(f'echo "{key}={item}" >> {rootfs}/etc/os-release')

        with open(f"{rootfs}/etc/X11/xinit/xinitrc", "r") as f:
            xinitrc = f.read().split("\n")

        with open(f"{rootfs}/etc/X11/xinit/xinitrc", "w") as f:
            f.write('\n'.join(xinitrc[0:-5] + ["exec sde"]))

        return 0
