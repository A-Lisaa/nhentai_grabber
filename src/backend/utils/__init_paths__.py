base_path = "."
appdata_path = f"{base_path}/__appdata__"
logs_path = f"{appdata_path}/log"
settings_path = f"{appdata_path}/settings.json"

def _show_paths():
    import os
    print(f"base_path = {os.path.abspath(base_path)}")
    print(f"appdata_path = {os.path.abspath(appdata_path)}")
    print(f"logs_path = {os.path.abspath(logs_path)}")
    print(f"settings_path = {os.path.abspath(settings_path)}")

if __name__ == "__main__":
    _show_paths()
