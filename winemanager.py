import os
import subprocess
import time

class WineManager:
    def __init__(self, root, wine_path, prefix_root):
        self.wine_path = wine_path
        self.prefix_root = prefix_root
        self.root = root

    def create_prefix(self, prefix_name):
        prefix_path = os.path.join(self.prefix_root, prefix_name)
        if os.path.exists(prefix_path):
            print("Prefix exists.")
            return
        else:
            environment = os.environ.copy()
            environment["WINEPREFIX"] = prefix_path

            subprocess.run([f'{self.wine_path}winecfg'], env=environment)
            os.system(f'cp {self.root}/dxvk/x64/*.dll {prefix_path}/drive_c/windows/system32')
            os.system(f'cp {self.root}/dxvk/x32/*.dll {prefix_path}/drive_c/windows/syswow64')
            

    def delete_prefix(self, prefix_name):
        prefix_path = os.path.join(self.prefix_root, prefix_name)
        if os.path.exists(prefix_path):
            os.system(f'sudo rm -rf "{prefix_path}"')
        else:
            print("Prefix doesn't exist.")

    def run(self, app_path, prefix_name, args, dlloverrides):
        prefix_path = os.path.join(self.prefix_root, prefix_name)
        app_name = os.path.basename(app_path)

        os.chdir(os.path.dirname(app_path))
        environment = os.environ.copy()
        environment["WINEPREFIX"] = prefix_path
        environment["WINEDLLOVERRIDES"] = dlloverrides
        environment["DXVK_HUD"] = "fps"

        subprocess.run([f'{self.wine_path}wine', f'"{app_name}"', f'{args}'], env=environment)

    def run_gptk(self, app_path, prefix_name, args, dlloverrides):
        prefix_path = os.path.join(self.prefix_root, prefix_name)
        app_name = os.path.basename(app_path)

        os.chdir(os.path.dirname(app_path))
        environment = os.environ.copy()
        environment["WINEPREFIX"] = prefix_path
        environment["WINEDLLOVERRIDES"] = dlloverrides
        environment["MTL_HUD_ENABLED"] = "1"

        subprocess.run([f'{self.wine_path}wine', f'"{app_name}"', f'{args}'], env=environment)

    def winecfg(self, prefix_name):
        prefix_path = os.path.join(self.prefix_root, prefix_name)
        
        environment = os.environ.copy()
        environment["WINEPREFIX"] = prefix_path

        subprocess.run([f'{self.wine_path}winecfg'], env=environment)

