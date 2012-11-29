@X = constant i32 3

; Definition of main function
define i32 @main() {
       
       %x = load i32* @X
       %result = mul i32 %x, 8
       ret i32 %result

}
