main:
#if yes
#for no
#if depth 1
#for depth 0
	mov x,%eax
	mov y,%ebx

	mov %eax,if_operand_x
	mov %ebx,if_operand_y
	mov $comparison_register_saving, %edi
	mov %eax, 0(%edi)
	mov %ebx, 4(%edi)
	mov $0, %eax
	mov $0, %ebx
	movb if_operand_x, %al
	movb $0,eq(%eax,1)
	movb if_operand_y, %al
	movb $4,eq(%eax,1)
	movb if_operand_x, %al
	movb eq(%eax,1), %bl
	mov %ebx, d1
	mov $comparison_register_saving, %edi
	mov %eax, 0(%edi)
	mov %ebx, 4(%edi)

	mov $ebx_ifd1,%edi
  	mov %ebx, 0(%edi)

	mov $ecx_ifd1,%edi
  	mov %ecx, 0(%edi)

	mov $edx_ifd1,%edi
  	mov %edx, 0(%edi)

if_egale:
	mov $3,%ecx
	mov $5,%edx

	mov $ebx_ifd1,%edi
  	mov %ebx, 1(%edi)

	mov $ecx_ifd1,%edi
  	mov %ecx, 1(%edi)

	mov $edx_ifd1,%edi
  	mov %edx, 1(%edi)

else_diferite:
	mov $ebx_ifd1,%edi
  	mov 0(%edi),%ebx

	mov $ecx_ifd1,%edi
  	mov 0(%edi),%ecx

	mov $ecx_ifd1,%edi
  	mov 0(%edi),%ecx

	mov $2,%ebx
	mov $18,%ecx
	mov $19,%edx
	mov $20,%ebx

	mov $ebx_ifd1,%edi
  	mov %ebx, 0(%edi)

	mov $ecx_ifd1,%edi
  	mov %ecx, 0(%edi)

	mov $edx_ifd1,%edi
  	mov %edx, 0(%edi)

	prepare‑selector %bl,d1 (astept lamuriri)

	update %ecx,d1 (astept lamuriri)
	update %edx,d1
	update %ebx,d1

exit:
	mov $1,%eax
	mov $0,%ebx
	int $0x80

