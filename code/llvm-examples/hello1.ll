; Declare the string constant as a global constant.
@str = internal constant [14 x i8] c"Hello, world!\00"

; External declaration of the puts function
declare i32 @puts(i8*)
declare i32 @addition(i32 %x, i32 %y)

; Definition of main function
define i32 @main()
{
  ; Call puts function to write out the string to stdout.
  call i32 @puts( i8* getelementptr ([14 x i8]* @str, i32 0,i32 0))
  ; Call the addition function
  call i32 @addition(i32 2, i32 4)
  ; Return with Value = 0
  ret i32 0
}
