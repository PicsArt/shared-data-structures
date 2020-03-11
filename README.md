# Shared Memory Data Structure
This package allows you to use your data structures like numpy arrays in the 
shared memory environment between two or more python processes. This library
simplifies the use of shared memory data structures as you don't need to manually
manage shared memory.

# E.g:
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

## Important !!!
## Always delete your data structures after use.
```python
from shared_ds import SharedArray

# Create shared memory and put you numpy array into that memory segment.
shared_np_array = SharedArray.from_array(np_array)

shm_descriptor = shared_np_array.to_json()

# Delete and release SHM after usage.
shared_np_array.destroy()
```

### Currently supported data structures:
- Numpy Array
