from utils.process_monitor import check_all_tracked_programs, check_new_processes, handle_processes_queue
from utils.file_operations import auto_save, remake_old_data
from utils.tray_icon import init_icon
from utils.config_operations import handle_config
from gui.stats_root import StatsRoot
import threading
import globals


def init_program() -> None:
    init_icon()

    threading.Thread(target=check_all_tracked_programs).start()
    threading.Thread(target=handle_processes_queue).start()
    threading.Thread(target=check_new_processes).start()
    if globals.config["max_autosaves"] > 0:
        threading.Thread(target=lambda: auto_save(globals.config["autosave_delay"],
                                                  globals.config["max_autosaves"]), daemon=True).start()


def main() -> None:
    remake_old_data()
    handle_config()
    globals.stats_root = StatsRoot()
    threading.Thread(target=init_program).start()
    globals.stats_root.mainloop()


if __name__ == "__main__":
    main()
