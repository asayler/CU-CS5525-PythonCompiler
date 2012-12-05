
define i32 @ftest(i32 %a) {
  ret i32 %a
}

define i32 @main() {
  %fptr1  = ptrtoint i32 (i32)* @ftest to i32
  %1      = call i32 @print_int_nl(i32 %fptr1)
  %fvars0 = call i32 @create_list(i32 0)
  %fvars1 = call i32 @inject_big(i32 %fvars0)
  %2      = call i32 @print_any(i32 %fvars1)
  %close0 = call i32 @create_closure(i32 %fptr1, i32 %fvars1)
  %close1 = call i32 @inject_big(i32 %close0)
  %fptr2  = call i32 @get_fun_ptr(i32 %close1)
  %3      = call i32 @print_int_nl(i32 %fptr2)
  %fptr3  = inttoptr i32 %fptr2 to i32 (i32)*
  %res0   = call i32 %fptr3(i32 5)
  %4      = call i32 @print_int_nl(i32 %res0)
  ret i32 0
}

