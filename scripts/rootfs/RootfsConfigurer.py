from scripts.Node import Node
from scripts.Config import Config
import scripts.Utilities as Utilities

import subprocess


class RootfsConfigurer(Node):
    def __init__(self, config, logger, rootfs_image):
        super().__init__("RootfsConfigurer")
        
        self.config: Config = config
        self.rootfs_image = rootfs_image
        self.log = logger.get_from_node(self)

    def configure(self) -> int:
        self.log.info("Configuring rootfs")

        chroot = subprocess.Popen(
            ["arch-chroot", self.rootfs_image.tmp_folder.get_path()],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )

        # chroot.stdin.write("passwd root\n".encode())
        # chroot.stdin.write(f"{self.config.values['root_password']}\n".encode())
        # chroot.stdin.write(f"{self.config.values['root_password']}\n".encode())

        chroot.kill()
        return 0
