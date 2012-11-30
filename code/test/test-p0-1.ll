; test-p0-1.ll

; void print_int_nl(int x);
declare void @print_int_nl(i32 %x)

;int input();
declare i32 @input()

; Definition of main function
define i32 @main() {
       
       %v0 = call i32 @input()
       %v1 = call i32 @input()
       %v2 = add i32 %v0, %v1
       call void @print_int_nl(i32 %v2)
       ret i32 0

}
