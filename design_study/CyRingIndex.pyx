# distutils: language = c++

cdef extern from "ReplayBuffer.hh" namespace "ymd":
    cdef cppclass ThreadSafeRingIndex:
        ThreadSafeRingIndex()
        ThreadSafeRingIndex(size_t)
        size_t fetch_add(size_t)

cdef class CyThreadSafeRingIndex:
    cdef ThreadSafeRingIndex* index

    def __cinit__(self,buffer_size):
        self.index = new ThreadSafeRingIndex(buffer_size)

    def fetch_add(self,i):
        return self.index.fetch_add(i)

    def __dealloc__(self):
        del self.index
