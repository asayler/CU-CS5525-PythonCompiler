define i64 @ftest(i64 %a) {
  ret i64 %a
}
define i64 @main() {
  %fptr1  = ptrtoint i64 (i64)* @ftest to i64
  %fvars0 = call i64 @create_list(i64 0)
  %fvars1 = call i64 @inject_big(i64 %fvars0)
  %close0 = call i64 @create_closure(i64 %fptr1, i64 %fvars1)
  %close1 = call i64 @inject_big(i64 %close0)
  %fptr2  = call i64 @get_fun_ptr(i64 %close1)
  %fptr3  = inttoptr i64 %fptr2 to i64 (i64)*
  %res0   = call i64 %fptr3(i64 5)
  ret i64 0
}