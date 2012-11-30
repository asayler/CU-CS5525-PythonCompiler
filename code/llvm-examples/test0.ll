
;int input();
declare i32 @input()

; Definition of main function
define i32 @main() {
       
       %v0 = call i32 @input()
       ret i32 0

}
