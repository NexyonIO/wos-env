import os

__COUNTER = 0


class TmpFolder:
    def __init__(self, fid) -> None:
        self.is_opened = True
        self.folder_name = f"tmp_{fid}"

        os.makedirs(f"tmp/{self.folder_name}", exist_ok=True)
    
    def is_available(self):
        return self.is_opened

    def get_path(self):
        return f"{os.getcwd()}/tmp/{self.folder_name}/"

    def close(self):
        self.is_opened = False
        os.system(f"rm -rf {self.get_path()}")


def create_tmp_folder() -> TmpFolder:
    global __COUNTER
    __COUNTER += 1
        
    os.makedirs("tmp", exist_ok=True)
    return TmpFolder(__COUNTER)
