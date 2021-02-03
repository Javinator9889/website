import logging
from datetime import datetime, timedelta
import subprocess
from time import sleep
from threading import Lock
from daemonize import Daemonize
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO,
                    filename="webserver-monitor.log")


class FSHandler(PatternMatchingEventHandler):
    def __init__(self, 
                 patterns=None, 
                 ignore_patterns=None,
                 ignore_directories=False, 
                 case_sensitive=False,
                 env_file=None):
        super().__init__(patterns=patterns, ignore_patterns=ignore_patterns,
                         ignore_directories=ignore_directories, case_sensitive=case_sensitive)
        if env_file is not None:
            vars = dict()
            with open(env_file, 'r') as file:
                for line in file:
                    if line.startswith('#') or not line.strip():
                        continue
                    key, value = line.strip().split('=', 1)
                    vars[key] = value
            logging.warning(vars)
            self.env = vars
        else:
            self.env = None
        self.lock = Lock()
        self.copying = False
        self.last_modified = datetime.now()

    @property
    def copying(self):
        with self.lock:
            return self.__copying

    @copying.setter
    def copying(self, value):
        with self.lock:
            self.__copying = value

    def on_created(self, _):
        return self.copy()

    def on_modified(self, _):
        return self.copy()

    def copy(self):
        if self.copying or datetime.now() - self.last_modified < timedelta(seconds=1):
            return
        try:
            self.copying = True
            self.last_modified = datetime.now()
            logging.warning("Running copy function")
            target_dir = self.env.get("TARGET_DIR") if self.env is not None else None
            logging.warning(target_dir)
            proc = subprocess.Popen(["rsync", "-avh", "--delete", "public/", "test/"],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            out, err = proc.communicate()
            if proc.returncode != 0:
                err = err.decode('utf-8').splitlines()
                for line in err:
                    logging.error(line)
            else:
                out = out.decode('utf-8').splitlines()
                for line in out:
                    logging.debug(line)
                logging.info('rsync completed successfully')
        except Exception as e:
            logging.error("Unexpected error!", e, stack_info=True)
        finally:
            self.copying = False


def launch_wd():
    logger = logging.getLogger()
    logger.warning("Starting watchdog...")
    event_handler = FSHandler(patterns="*.version", env_file=".env")
    observer = Observer()
    observer.schedule(event_handler, '.', recursive=False)
    observer.start()
    try:
        while True:
            sleep(1)
    finally:
        observer.stop()
        observer.join()


if __name__ == '__main__':
    logger = logging.getLogger()
    fds = [handler.stream.fileno() for handler in logger.handlers if isinstance(handler, logging.FileHandler)]
    daemon = Daemonize(app="webmonit", pid="./monit.pid", action=launch_wd, logger=logging, keep_fds=fds, chdir='.')
    daemon.start()
