
Notes:

Helpful scripts
Reverse bits
This script will reverse the bit ordering in one byte (if you are not able to change LSB / MSB
first to your needs.
```python
def ReverseBits(byte):
 byte = ((byte & 0xF0) >> 4) | ((byte & 0x0F) << 4)
 byte = ((byte & 0xCC) >> 2) | ((byte & 0x33) << 2)
 byte = ((byte & 0xAA) >> 1) | ((byte & 0x55) << 1)
 return byte
```

Print bytes
This script will print out a byte array in a human readable format (hexadecimal). This is often
useful during debugging.
```python
def BytesToHex(Bytes):
 return ''.join(["0x%02X " % x for x in Bytes]).strip()
```
