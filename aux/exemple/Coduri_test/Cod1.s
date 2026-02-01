.data
	v: .long 1,1,1,1,1
	n: .long 5
.text
.global main
main:
	lea v,%edi
	mov $0,%ecx
	mov $0,%eax
loop:
	cmp n,%ecx
	je exit
	mov (%edi,%ecx,4),%edx
	add %edx,%eax
	inc %ecx
	jmp loop
exit:
	mov $1,%eax
	xor %ebx,%ebx
	int $0x80
