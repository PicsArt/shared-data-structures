import pytest
from io import BytesIO
from multiprocessing import Process, Queue

from src.shared_ds import SharedBytesIO


def process_2(shared_memory_descriptor, queue):
    shared_mem_data = SharedBytesIO.from_json(shared_memory_descriptor).get_data()
    queue.put(shared_mem_data)


class Test(object):
    def test_wrong_object_type(self):
        wrong_param = 12345
        with pytest.raises(ValueError):
            SharedBytesIO.from_bytes_io(wrong_param)

    def test_shared_bytes_io(self):
        data = BytesIO(b'test_data')

        shared_mem_obj = SharedBytesIO.from_bytes_io(data)
        sm_descriptor = shared_mem_obj.to_json()

        result_queue = Queue()

        p = Process(target=process_2, args=(sm_descriptor, result_queue))
        p.start()
        p.join()

        assert 'test_data' == result_queue.get().decode('utf-8')
