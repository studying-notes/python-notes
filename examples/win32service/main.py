import multiprocessing
import os
import sys
import time

import servicemanager
import win32event
import win32service
import win32serviceutil


def run():
    while True:
        print(
            time.strftime(
                "%Y-%m-%d %H:%M:%S",
                time.localtime(),
            )
        )
        time.sleep(1)


class WindowsServiceApp(win32serviceutil.ServiceFramework):
    _svc_name_ = "名称"
    _svc_display_name_ = "显示名称"
    _svc_description_ = "详细描述"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, ""),
        )

        # determine if application is a script file or frozen exe
        if getattr(sys, "frozen", False):
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(__file__)

        process = multiprocessing.Process(target=run)
        process.start()

        print("Process started with pid %d, in %s" % (process.pid, application_path))

        while True:
            rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)
            if rc == win32event.WAIT_OBJECT_0:
                process.kill()
                break


if __name__ == "__main__":
    from multiprocessing import freeze_support

    # https://github.com/pyinstaller/pyinstaller/issues/2023
    freeze_support()

    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(WindowsServiceApp)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(WindowsServiceApp)
