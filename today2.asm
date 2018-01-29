section .data
	a dd 1
	b dd 5
	c dd 15
	k dq 2.3
	msg db "rahul chavan"

section .bss
	m resd 1
	d resb 1

section .text
	global main
	extern printf

main:
	mov eax,dword[a]
	mov ebx,dword[b]
	mov ax,bx
	mov ah,al
	mov bh,k
	mov ch,'z'
	mov dh,7
	mov eax,3
	mov ecx,15
	mov eax,'r'
	mov ebx,dword[c]
	add eax,ebx
abc:
	push eax
	push msg
	call printf
	add esp,8
	jmp pqr
	
