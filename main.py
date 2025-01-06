from utils.process_monitor import check_all_tracked_programs, check_new_processes, handle_processes_queue
from utils.file_operations import auto_save, remake_old_data
from utils.tray_icon import init_icon
from gui.stats_root import StatsRoot
import threading
import globals


def init_program() -> None:
    check_all_tracked_programs()
    init_icon()

    threading.Thread(target=handle_processes_queue).start()
    threading.Thread(target=check_new_processes).start()
    threading.Thread(target=lambda: auto_save(1, 7), daemon=True).start()


def main() -> None:
    remake_old_data()
    globals.stats_root = StatsRoot()
    threading.Thread(target=init_program).start()
    globals.stats_root.mainloop()


if __name__ == "__main__":
    main()
