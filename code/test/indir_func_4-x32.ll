declare i32 @print_int_nl(i32)
declare i32 @print_any(i32)
declare i32 @input()
declare i32 @input_int()
declare i32 @inject_int(i32)
declare i32 @inject_bool(i32)
declare i32 @inject_big(i32)
declare i32 @project_int(i32)
declare i32 @project_bool(i32)
declare i32 @project_big(i32)
declare i32 @is_true(i32)
declare i32 @tag(i32)
declare i32 @error_pyobj()
declare i32 @is_int(i32)
declare i32 @is_bool(i32)
declare i32 @is_big(i32)
declare i32 @is_function(i32)
declare i32 @is_object(i32)
declare i32 @is_class(i32)
declare i32 @is_unbound_method(i32)
declare i32 @is_bound_method(i32)
declare i32 @create_list(i32)
declare i32 @create_dict()
declare i32 @set_subscript(i32, i32, i32)
declare i32 @get_subscript(i32, i32)
declare i32 @add(i32, i32)
declare i32 @equal(i32, i32)
declare i32 @not_equal(i32, i32)
declare i32 @create_closure(i32, i32)
declare i32 @get_fun_ptr(i32)
declare i32 @get_free_vars(i32)
declare i32 @set_free_vars(i32, i32)

define i32 @ftest(i32 %a) {
  %1 = alloca i32
  store i32 %a, i32* %1
  %2 = load i32* %1
  ret i32 %2
}

define i32 @main() {
  %1 = alloca i32
  %func = alloca i32 (i32)*
  %anyv = alloca i8*
  store i32 0, i32* %1
  store i8* bitcast (i32 (i32)* @ftest to i8*), i8** %anyv
  %2 = load i8** %anyv
  %3 = bitcast i8* %2 to i32 (i32)*
  store i32 (i32)* %3, i32 (i32)** %func
  %fptr0  = load i32 (i32)** %func
  %fptr1  = ptrtoint i32 (i32)* %fptr0 to i32
  %4      = call i32 @print_int_nl(i32 %fptr1)
  %fvars0 = call i32 @create_list(i32 0)
  %fvars1 = call i32 @inject_big(i32 %fvars0)
  %5      = call i32 @print_any(i32 %fvars1)
  %close0 = call i32 @create_closure(i32 %fptr1, i32 %fvars1)
  %close1 = call i32 @inject_big(i32 %close0)
  %fptr2  = call i32 @get_fun_ptr(i32 %close1)
  %6      = call i32 @print_int_nl(i32 %fptr2)
  %fptr3  = inttoptr i32 %fptr2 to i32 (i32)*
  %res0   = call i32 %fptr3(i32 5)
  %7      = call i32 @print_int_nl(i32 %res0)
  ret i32 0
}
