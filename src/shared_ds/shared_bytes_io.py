import json
import mmap
import posix_ipc
import sys
import uuid
from io import BytesIO


class SharedBytesIO(object):
    def __init__(self, shared_memory, mem_buffer, bytes_count):
        self.shared_memory = shared_memory
        self.memory_buffer = mem_buffer
        self.bytes_count = bytes_count

    @classmethod
    def from_bytes_io(cls, bytes_io_obj):
        if type(bytes_io_obj) is BytesIO:
            shared_mem_uuid = str(uuid.uuid4())[16:]

            bytes_count = bytes_io_obj.getbuffer().nbytes

            shared_memory = posix_ipc.SharedMemory(name=shared_mem_uuid,
                                                   flags=posix_ipc.O_CREX,
                                                   size=bytes_count,
                                                   read_only=False)

            mem_buffer = mmap.mmap(shared_memory.fd, shared_memory.size)
            mem_buffer.write(bytes_io_obj.read())

            return cls(shared_memory, mem_buffer, bytes_count)
        else:
            raise ValueError('Invalid data format')

    def to_json(self):
        return json.dumps({'shared_mem_uuid': self.shared_memory.name, 'size': self.bytes_count})

    @classmethod
    def from_json(cls, json_string):
        shared_memory_params = json.loads(json_string)
        shared_mem_uu_id = shared_memory_params.get('shared_mem_uuid', None)
        bytes_count = shared_memory_params.get('size', 0)
        if shared_mem_uu_id:
            shared_memory = posix_ipc.SharedMemory(name=shared_mem_uu_id,
                                                   flags=posix_ipc.O_CREAT,
                                                   read_only=False)

            memory_buffer = mmap.mmap(shared_memory.fd, shared_memory.size)
            return cls(shared_memory, memory_buffer, bytes_count)

    def __unlink(self):
        """
        Closes memory_buffer and memory_descriptor.
        @return: None
        @rtype: None
        """
        self.memory_buffer.close()
        self.shared_memory.close_fd()

    def destroy(self):
        """
        Order operating system to destroy allocated shared memory.
        Important you should always destroy shared_memory after use. Otherwise
        you will have memory leak. This should be called by master process,
        otherwise child processes can destroy it without waiting for other
        processes to read the information.
        @return: None
        @rtype: None
        """
        posix_ipc.unlink_shared_memory(self.shared_memory.name)

    def get_data(self):
        return self.memory_buffer.read(self.bytes_count)
    
    def __del__(self):
        self.__unlink()
