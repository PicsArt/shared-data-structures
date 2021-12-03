# Shared Memory Data Structure
This package allows you to use your data structures like numpy arrays in the 
shared memory environment between two or more python processes. This library
simplifies the use of shared memory data structures as you don't need to manually
manage shared memory.

# SharedArray example:
## Process #1
```python
from shared_ds import SharedArray

# Create shared memory and put you numpy array into that memory segment.
shared_np_array = SharedArray.from_array(np_array)

shm_descriptor = shared_np_array.to_json()

```
## Process #2
```python
from shared_ds import SharedArray

# Attaches to existing shared memory and reads numpy array representation.
shared_np_array = SharedArray.from_json(shm_descriptor)

shm_descriptor = shared_np_array.to_json()

```

# io.BytesIO example:
## Process #1
```python
from shared_ds import SharedBytesIO
import io

# Create shared memory and put content of passed BytesIO into that memory segment.
data_to_store = io.BytesIO(b'data which we want to store')
shared_memory = SharedBytesIO.from_bytes_io(data_to_store)

shm_descriptor = shared_memory.to_json()

```
## Process #2
```python
from shared_ds import SharedBytesIO

# Attaches to existing shared memory and gets io.BytesIO content.
shared_memory = SharedBytesIO.from_json(shm_descriptor)

data = shared_memory.get_data()

```

### Currently supported data structures:
- Numpy Array
- io.BytesIO
