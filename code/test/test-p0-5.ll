; External declaration of linked functions
declare void @print_int_nl(i32 %x)

@V1 = constant i32 1

; Definition of main function
define i32 @main()
{
  ;x = 1
  %v1 = load i32* @V1
  ;print(x + 2)
  %v2 = add i32 %v1, 2
  call void @print_int_nl(i32 %v2)

  ret i32 0
}




