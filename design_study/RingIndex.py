import time
from multiprocessing import Lock
import platform

import pyximport

# https://stackoverflow.com/questions/21938065/how-to-configure-pyximport-to-always-make-a-cpp-file
old_get_distutils_extension = pyximport.pyximport.get_distutils_extension

def new_get_distutils_extension(modname, pyxfilename, language_level=None):
    extension_mod, setup_args = old_get_distutils_extension(modname, pyxfilename, language_level)
    extension_mod.language='c++'

    if platform.system() != 'Windows':
        extension_mod.extra_compile_args = ["-std=c++17"]
        extension_mod.extra_liink_args = ["-std=c++17","-pthread"]
    else:
        extension_mod.extra_compile_args = ["/std:c++17"]
    return extension_mod,setup_args

pyximport.pyximport.get_distutils_extension = new_get_distutils_extension

pyximport.install(language_level=3,
                  inplace=True,
                  setup_args={'include_dirs':['../cpprb']})

from CyRingIndex import CyThreadSafeRingIndex


class Stat:
    def __init__(self):
        self.N = 0
        self.x = 0.0
        self.xx = 0.0
        pass

    def Add(self,y):
        self.N += 1
        self.x += y
        self.xx += y*y
        return None

    def Average(self):
        return self.x/self.N

    def Std(self):
        ave = self.Average()
        return (self.xx/self.N - ave*ave)

    def stat(self,*,name=None):
        print(f"{name}: {self.Average()} +/- {self.Std()} s")


def main():
    N = 10000
    M = 1000

    buffer_size = 10240
    lock = Lock()

    index = 0
    py_stat = Stat()

    cpp_index = CyThreadSafeRingIndex(buffer_size)
    cpp_stat = Stat()

    for _ in range(M):
        start = time.perf_counter()
        for i in range(N):
            lock.acquire()
            index += i
            while index >= buffer_size:
                index -= buffer_size
            lock.release()
        end = time.perf_counter()
        py_stat.Add(end - start)


        start = time.perf_counter()
        for i in range(N):
            cpp_index.fetch_add(i)
        end = time.perf_counter()
        cpp_stat.Add(end - start)

    py_stat.stat( name="Python Lock         ")
    cpp_stat.stat(name="C++ Atomic Operation")



if __name__ == "__main__":
    main()
