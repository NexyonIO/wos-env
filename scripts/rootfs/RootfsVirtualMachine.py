from scripts.grub.BootableIso import BootableIso
from scripts.Config import Config
from scripts.Node import Node
import scripts.Utilities as Utilities


class RootfsVirtualMachine(Node):
    def __init__(self, config, logger, bootable: BootableIso):
        super().__init__("RootfsVirtualMachine")
        
        self.config: Config = config
        self.bootable: BootableIso = bootable
        self.log = logger.get_from_node(self)

    def __flags(self):
        flags = []

        if self.config.values['vm_kvm']:
            flags.append("-accel kvm")

        return ' '.join(flags)

    def run_vm(self):
        if not Utilities.is_tool("qemu-system-x86_64"):
            self.log.panic("qemu-system-x86_64 should be installed for the VM to start.")
            self.log.panic("Consider installing qemu package 'qemu-full' via pacman", exit_code=1)

        self.run_command(f"qemu-system-x86_64 -m 2G -cdrom {self.bootable.iso_path} {self.__flags()}")
