__version__ = "3.2"

default_runned_apps: list = ["python.exe", "dllhost.exe", "RuntimeBroker.exe", "svchost.exe", "conhost.exe",
                             "SearchProtocolHost.exe", "backgroundTaskHost.exe", "smartscreen.exe", "FileCoAuth.exe",
                             "runnerw.exe", "git.exe", "GameBarPresenceWriter.exe"]
wait_for_write_data: bool = False
requested_to_quit: bool = False
new_processes_queue: dict = {}
stats_root = None
icon = None
