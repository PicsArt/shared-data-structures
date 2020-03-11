# Shared Memory Data Structure
This package allows you to use your data structures like numpy arrays in the 
shared memory environment between two or more python processes.

# E.g:
```python
from shared_ds import SharedArray

# Create shared memory and put you numpy array into that memory segment.
shared_np_array = SharedArray.from_array(np_array)

```

### Currently supported data structures:
- Numpy Array
