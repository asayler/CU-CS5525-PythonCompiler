declare i64 @print_int_nl(i64)
declare i64 @print_any(i64)
declare i64 @input()
declare i64 @input_int()
declare i64 @inject_int(i64)
declare i64 @inject_bool(i64)
declare i64 @inject_big(i64)
declare i64 @project_int(i64)
declare i64 @project_bool(i64)
declare i64 @project_big(i64)
declare i64 @is_true(i64)
declare i64 @tag(i64)
declare i64 @error_pyobj()
declare i64 @is_int(i64)
declare i64 @is_bool(i64)
declare i64 @is_big(i64)
declare i64 @is_function(i64)
declare i64 @is_object(i64)
declare i64 @is_class(i64)
declare i64 @is_unbound_method(i64)
declare i64 @is_bound_method(i64)
declare i64 @create_list(i64)
declare i64 @create_dict()
declare i64 @set_subscript(i64, i64, i64)
declare i64 @get_subscript(i64, i64)
declare i64 @add(i64, i64)
declare i64 @equal(i64, i64)
declare i64 @not_equal(i64, i64)
declare i64 @create_closure(i64, i64)
declare i64 @get_fun_ptr(i64)
declare i64 @get_free_vars(i64)
declare i64 @set_free_vars(i64, i64)

define i64 @ftest(i64 %a) {
  %1 = alloca i64
  store i64 %a, i64* %1
  %2 = load i64* %1
  ret i64 %2
}

define i64 @main() {
  %func = alloca i64 (i64)*
  store i64 (i64)* @ftest, i64 (i64)** %func
  %fptr0  = load i64 (i64)** %func
  %fptr1  = ptrtoint i64 (i64)* %fptr0 to i64
  %1      = call i64 @print_int_nl(i64 %fptr1)
  %fvars0 = call i64 @create_list(i64 0)
  %fvars1 = call i64 @inject_big(i64 %fvars0)
  %2      = call i64 @print_any(i64 %fvars1)
  %close0 = call i64 @create_closure(i64 %fptr1, i64 %fvars1)
  %close1 = call i64 @inject_big(i64 %close0)
  %fptr2  = call i64 @get_fun_ptr(i64 %close1)
  %3      = call i64 @print_int_nl(i64 %fptr2)
  %fptr3  = inttoptr i64 %fptr2 to i64 (i64)*
  %res0   = call i64 %fptr3(i64 5)
  %4      = call i64 @print_int_nl(i64 %res0)
  ret i64 0
}
