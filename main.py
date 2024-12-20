import winemanager
import json
import time
import os

with open('settings.json', 'r') as file:
    programs = json.load(file)["programs"]
with open('settings.json', 'r') as file: 
    prefixes = json.load(file)["prefixes"]

config = json.load(open('config.json', 'r'))
prefix_path = config["PREFIX_PATH"]

manager = winemanager.WineManager(config["ROOT_PATH"], config["WINE_BIN_PATH"], prefix_path)
d3dmetal_manager = winemanager.WineManager(config["ROOT_PATH"], config["WINE_D3D_BIN_PATH"], prefix_path)

class MenuFramework:
    def __init__(self, title, options):
        """
        Initialize the menu with a title and a list of options.
        Each option should be a dictionary with keys 'label', 'action', and optional 'submenu'.
        """
        self.title = title
        self.options = options

    def display_menu(self):
        """Display the menu and return the user's choice."""
        os.system('clear')
        print(f"\n{self.title}")
        print("-" * len(self.title))
        for idx, option in enumerate(self.options, start=1):
            print(f"{idx}. {option['label']}")
        print("0. Exit")

        # Get user input
        while True:
            try:
                choice = int(input(": "))
                if 0 <= choice <= len(self.options):
                    return choice
                else:
                    print("Invalid choice. Try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def run(self):
        """Run the menu loop until the user exits."""
        while True:
            choice = self.display_menu()

            if choice == 0:
                print("Exiting... Goodbye!")
                break

            selected_option = self.options[choice - 1]
            action = selected_option.get("action")
            submenu = selected_option.get("submenu")

            if submenu:
                # Run a submenu if it exists
                submenu.run()
            elif action:
                # Call the action function
                action()
            else:
                print("No action defined for this option. Moving back to the menu.")
            
            os.system('clear')

def WinToUnix(path, c_drive_path):
    return path.replace("\\", "/").replace("C:", c_drive_path, 1)

# Run a Program
def run_program():
    os.system('clear')
    print("Choose a program: ")
    print("-----------------")
    for x in programs:
        print(f"{x}")

    program = programs[input("Choose a Program: ")]
    if program["Settings"]["Renderer"] == "D3DMetal":
        d3dmetal_manager.run_gptk(program["Path"], prefixes[program["Prefix"]], input("arguments: "), "")
    else:
        manager.run(program["Path"], prefixes[program["Prefix"]], input("arguments: "), "d3d10core,d3d11=n,b" if program["Settings"]["Renderer"] == "DXVK" else "")

# Manage Prefixes
def create_prefix():
    prefix_name = input("Enter a prefix name: ")
    manager.create_prefix(prefix_name)
    prefixes[prefix_name] = prefix_name

def delete_prefix():
    for x in prefixes:
        print(x)

    prefix_name = input("Enter the prefix name: ")
    if prefix_name in prefixes:
        manager.delete_prefix(prefix_name)
        del prefixes[prefix_name]
    else:
        print('Prefix does not exist... ')
        input(': ')

def winecfg():
    for x in prefixes:
        print(x)

    manager.winecfg(input("Enter the prefix name: "))

# Manage Shortcuts
def create_shortcut():
    shortcut_name = input("Enter the name of the shortcut: ")
    for x in prefixes:
        print(f"{x}")
    shortcut_prefix = input("Prefix to use: ")
    if shortcut_prefix not in prefixes:
        shortcut_prefix = input("Prefix doesn't exist. Try again: ")
    shortcut_path_untreated = input("Location of EXE file: ")
    if shortcut_path_untreated[:2] == "C:":
        shortcut_path = WinToUnix(shortcut_path_untreated, f'{prefix_path}{shortcut_prefix}/drive_c')

    programs[shortcut_name] = dict(Path = shortcut_path, Prefix = shortcut_prefix, Settings = dict(Renderer = "None"))

def delete_shortcut():
    print("This will only delete the shortcut, and will not delete the program from disk.")
    shortcut_name = input("Enter the name of the shortcut: ")
    for x in programs:
        print(x)

    if shortcut_name in programs:
        del programs[shortcut_name]
    else:
        print("That shortcut does not exist. Try again. ")

def graphics_shortcut():
    for x in programs: print(x)
    chosen_program = input("What shortcut would you like to edit? ")
    print("What Graphics Backend would you like to use? DXVK or D3DMetal")
    programs[chosen_program]["Settings"]["Renderer"] = input(": ")

# Define the main menu and submenu options
def main():
    # Submenus
    manage_prefixes_menu = MenuFramework("Manage Prefixes", [
        {"label": "Create a Prefix", "action": create_prefix},
        {"label": "Delete a Prefix", "action": delete_prefix},
        {"label": "Wine Configuration", "action": winecfg}
    ])

    manage_shortcuts_menu = MenuFramework("Manage Shortcuts", [
        {"label": "Create a Shortcut", "action": create_shortcut},
        {"label": "Delete Shortcut", "action": delete_shortcut},
        {"label": "Graphics Options", "action": graphics_shortcut}
    ])
    # Main Menu
    main_menu = MenuFramework("Main Menu", [
        {"label": "Run Program", "action": run_program},
        {"label": "Manage Prefixes", "submenu": manage_prefixes_menu},
        {"label": "Manage Shortcuts", "submenu": manage_shortcuts_menu}
    ])

    main_menu.run()


if __name__ == "__main__":
    main()
    data = dict(programs = programs, prefixes = prefixes)
    with open('settings.json', 'w') as file:
        json.dump(data, file)
