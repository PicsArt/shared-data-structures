import posix_ipc
import mmap
import numpy as np
import uuid
import json

numpy_types = {
    "bool": np.bool,
    "bool8": np.bool8,
    "bool_": np.bool_,

    "uint8": np.uint8,
    "uint16": np.uint16,
    "uint32": np.uint32,
    "uint64": np.uint64,

    "int_": np.int_,
    "intc": np.intc,
    "intp": np.intp,
    "int": np.int,
    "int8": np.int8,
    "int16": np.int16,
    "int32": np.int32,
    "int64": np.int64,

    "float_": np.float_,
    "float": np.float,
    "float16": np.float16,
    "float32": np.float32,
    "float64": np.float64,
    "float128": np.float128,

    "complex64": np.complex64,
    "complex128": np.complex128,

}


class SharedArray(object):

    def __init__(self, data, shared_memory, memory_buffer):
        self.shared_memory = shared_memory
        self.memory_buffer = memory_buffer
        self.data = data

    def to_json(self):
        metadata = {"shared_mem_uuid": self.shared_memory.name,
                    "shape": self.data.shape,
                    "data_type": self.data.dtype.name}
        return json.dumps(metadata)

    @classmethod
    def from_json(cls, json_string):
        params = json.loads(json_string)
        shared_memory = posix_ipc.SharedMemory(name=params["shared_mem_uuid"],
                                               flags=posix_ipc.O_CREAT,
                                               read_only=False)
        memory_buffer = mmap.mmap(shared_memory.fd, shared_memory.size)
        data = np.ndarray(buffer=memory_buffer,
                          dtype=numpy_types[params["data_type"]],
                          shape=params["shape"])

        return cls(data=data,
                   shared_memory=shared_memory,
                   memory_buffer=memory_buffer)

    @classmethod
    def from_array(cls, array: np.ndarray):
        shared_mem_uuid = str(uuid.uuid4())[16:]

        shared_memory = posix_ipc.SharedMemory(name=shared_mem_uuid, flags=posix_ipc.O_CREX, size=array.nbytes, read_only=False)
        memory_buffer = mmap.mmap(shared_memory.fd, shared_memory.size)
        memory_buffer.write(array.data)

        data = np.ndarray(buffer=memory_buffer,
                          dtype=array.dtype,
                          shape=array.shape)
        return cls(data=data,
                   shared_memory=shared_memory,
                   memory_buffer=memory_buffer)

    def get_data(self):
        return np.copy(self.data)

    def unlink(self):
        self.memory_buffer.close()
        self.shared_memory.close_fd()

    def destroy(self):
        posix_ipc.unlink_shared_memory(self.shared_memory.name)

    def __del__(self):
        self.unlink()
