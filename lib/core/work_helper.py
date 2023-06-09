
import threading
import collections
import time

class WorkHelper(object):
    def __init__(self, targets, concurrency=6):
        self.concurrency = concurrency
        self.semaphore = threading.Semaphore(concurrency)
        self._targets = targets
        self.result_list = []

    def work(self, target):
        raise NotImplementedError()

    def _work(self, target):
        try:
            ret_val = self.work(target)
            if ret_val:
                self.result_list.append(ret_val)
        except Exception as ex:
            # print(f"target:{target} [+] ", ex)
            pass

        except BaseException as ex:
            print("BaseException on {}".format(str(ex)))
            self.semaphore.release()
            raise ex
        self.semaphore.release()

    def _run(self):
        deque = collections.deque()
        for target in self._targets:
            if isinstance(target, str):
                target = target.strip()
            if not target:
                continue
            self.semaphore.acquire()
            t1 = threading.Thread(target=self._work, args=(target,))
            t1.start()
            deque.append(t1)

        for t in list(deque):
            while t.is_alive():
                time.sleep(0.2)
    
    def run(self):
        self._run()
        return self.result_list
