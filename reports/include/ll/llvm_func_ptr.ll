define i64 @ftest(i64 %a) {
  ret i64 %a
}
define i64 @main() {
  %fptr1  = ptrtoint i64 (i64)* @ftest to i64 ;Convert pointer to long int
  %fvars0 = call i64 @create_list(i64 0)
  %fvars1 = call i64 @inject_big(i64 %fvars0)
  %close0 = call i64 @create_closure(i64 %fptr1, i64 %fvars1) ;use this int in create closure
  %close1 = call i64 @inject_big(i64 %close0)
  %fptr2  = call i64 @get_fun_ptr(i64 %close1) ;get function ptr as i64
  %fptr3  = inttoptr i64 %fptr2 to i64 (i64)* ;convert to a ptr to make the call
  %res0   = call i64 %fptr3(i64 5)
  ret i64 0
}