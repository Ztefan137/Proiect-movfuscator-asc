.data
.text
.global main
main:
  mov $0,%eax
  mov $1,%ebx
  cmp %eax,%ebx
  je egale
diferite:
  mov $0,%ecx
  jmp exit
egale:
  mov $1,%ecx
exit:
  mov $0,%eax
  xor %ebx,%ebx
  int $0x80
