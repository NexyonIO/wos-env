from scripts.Logger import Logger
from scripts.Node import Node
from scripts.Config import Config
from scripts.rootfs.RootfsConfigurer import RootfsConfigurer

import scripts.tmp.TmpUtils as TmpUtils
import scripts.Utilities as Utilities

import os
import time


class RootfsImage(Node):
    def __init__(self, config, log, image_path, squashfs_file, size=2048):
        super().__init__("RootfsImage")

        self.config: Config = config
        self.logger: Logger = log.get_from_node(self)
        self.configurer: RootfsConfigurer = RootfsConfigurer(config, log, self)

        self.image_path = image_path
        self.squashfs_file = squashfs_file
        self.size = size
        self.tmp_folder = TmpUtils.create_tmp_folder()
        self.packages = []
        self.mounted = False

        self.add_package("linux")
        self.add_package("linux-firmware")
        self.add_package("base")
        self.add_package("vim")
        self.add_package("sudo")
        self.add_package("nano")
        self.add_package("dhclient")
        self.add_package("which")
        self.add_package("curl")
        self.add_package("wget")
        self.add_package("grub")
        self.add_package("efibootmgr")

        for pkg in self.config.values['additional_packages']:
            self.add_package(pkg)

    def add_package(self, pkg):
        self.packages.append(pkg)

    def close(self):
        self.logger.info("Cleaning up")
        self.umount(self.tmp_folder.get_path())
        self.tmp_folder.close()

    def allocate(self, image):
        self.logger.info("Allocating image file", image, f"with size of {(self.size / 1024)}GB")
        return self.run_command(f"dd if=/dev/zero of={image} bs=1M count={round(self.size)} status=progress")

    def format(self, image):
        self.logger.info("Formating image file", image)
        return self.run_command(f"mke2fs -F {image}")

    def mount(self, image, location):
        self.logger.info("Mounting image file", image, f"at {location}")
        code = self.run_command(f"mount -o loop {image} {location}")

        if code == 0:
            self.mounted = True

        return code

    def umount(self, location):
        if not self.mounted:
            return 0
        
        self.logger.info(f"Unmounting rootfs at {location}")
        code = 1
        
        while code != 0:
            code = self.run_command(f"umount -l {location}")

            if code != 0:
                self.logger.warn("Waiting for rootfs to unmount...")
                time.sleep(3)
        
        self.mounted = False
        return code

    def install_rootfs(self, mount_location):
        self.logger.info("Installing rootfs at", mount_location)
        code =  self.run_commands(
            f"pacstrap -K {mount_location} {' '.join(self.packages)}",
        )

        return code

    def create_squashfs(self, squashfs_file, mount_location):
        self.logger.info("Creating squashfs from", mount_location)
        return self.run_command(f"mksquashfs {mount_location} {squashfs_file}")

    def setup_image(self):
        self.logger.info("Setting up rootfs image at", self.image_path)
        
        if os.path.isfile(".rootfs_ready") and os.path.isfile(self.squashfs_file):
            user_input = Utilities.ask_user(
                "Rootfs is already configured. Do you want to skip this step?",
                ('Y', 'N')
            )

            if user_input == 'Y':
                return 0
            
            self.run_command("rm .rootfs_ready")

        assert self.allocate(self.image_path) == 0, "Unable to allocate image disk"
        assert self.format(self.image_path) == 0, "Unable to format image disk"
        assert self.mount(self.image_path, self.tmp_folder.get_path()) == 0, "Unable to mount image disk"
        self.install_rootfs(self.tmp_folder.get_path())
        input()
        assert self.configurer.configure() == 0, "Unable to configure rootfs"
        assert self.create_squashfs(self.squashfs_file, self.tmp_folder.get_path()) == 0, "Unable to create squashfs disk"
        assert self.umount(self.tmp_folder.get_path()) == 0, "Unable to umount image disk"
        assert self.run_command(f"rm {self.image_path}") == 0, "Unable to remove image disk"

        self.run_command("touch .rootfs_ready")

        return 0
