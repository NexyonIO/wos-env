from scripts.rootfs.RootfsImage import RootfsImage
from scripts.Node import Node
import scripts.Utilities as Utilities


class BootableIso(Node):
    def __init__(self, logger, iso_path, rootfs_image: RootfsImage):
        super().__init__("BootableIso")
        
        self.iso_path = iso_path
        self.rootfs_image: RootfsImage = rootfs_image
        self.log = logger.get_from_node(self)

        self.iso_label = "WOS_ISO"

    def create_iso(self):
        self.run_commands(
            f"mv {self.rootfs_image.squashfs_file} iso/arch/x86_64/airootfs.sfs",
            f"grub-mkrescue -V {self.iso_label} -o {self.iso_path} iso",
            f"mv iso/arch/x86_64/airootfs.sfs {self.rootfs_image.squashfs_file}",
        )
