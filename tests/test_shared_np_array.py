from shared_ds import SharedArray
import numpy as np
from hashlib import sha1
from concurrent.futures import ProcessPoolExecutor
import pytest

def process2(shm_descriptor, array_checksum):
    np_array_r = SharedArray.from_json(shm_descriptor).get_data()
    checksum = sha1(np_array_r).hexdigest()
    # is_right = checksum == array_checksum
    return array_checksum


def test_correctness():
    np_array = np.random.rand(2000, 2000 ,3)
    shm_array = SharedArray.from_array(np_array)
    checksum = sha1(np_array).hexdigest()
    executor = ProcessPoolExecutor()
    future = executor.submit(fn=process2,
                             shm_descriptor=shm_array.to_json(),
                             array_checksum=checksum)

    process2_checksum = future.result()
    assert checksum == process2_checksum


def test_from_array_params():
    fake_np_array = [1, 2, 3, 4, 5, 6]
    with pytest.raises(ValueError):
        SharedArray.from_array(fake_np_array)
