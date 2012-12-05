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
declare i64 @error_pyobj();
declare i64 @is_int(i64);
declare i64 @is_bool(i64);
declare i64 @is_big(i64);
declare i64 @is_function(i64);
declare i64 @is_object(i64);
declare i64 @is_class(i64);
declare i64 @is_unbound_method(i64);
declare i64 @is_bound_method(i64);
declare i64 @create_list(i64);
declare i64 @create_dict();
declare i64 @set_subscript(i64, i64, i64);
declare i64 @get_subscript(i64, i64);
declare i64 @add(i64, i64);
declare i64 @equal(i64, i64);
declare i64 @not_equal(i64, i64);

declare i64 @create_closure(i8*, i64);
declare i64 @get_fun_ptr(i64);
declare i64 @get_free_vars(i64);
declare i64 @set_free_vars(i64, i64);

define void @lamda(i64 %x){

  call i64 @print_any(i64 %x)
  ret void

}

; Definition of main function
define i32 @main() {

  %n_2_callfunctmp$0 = call i64 @inject_int(i64 0)
  %n_3_callfunctmp$0 = call i64 @create_list(i64 %n_2_callfunctmp$0)
  %n_1_x$0 = call i64 @inject_big(i64 %n_3_callfunctmp$0)
 

  %1 = alloca i32
  %func = alloca i32 (i32)*
  %anyv = alloca i8*
  store i32 0, i32* %1
  store i8* bitcast (i32 (i32)* @lambda to i8*), i8** %anyv
  %2 = load i8** %anyv
  %3 = bitcast i8* %2 to i32 (i32)*
  store i32 (i32)* %3, i32 (i32)** %func
  %4 = load i32 (i32)** %func

  %f = call i64 @create_closure(i8* %2, i64 %n_1_x$0)


  

  ;f = create closure(lambda_1, [])
  ;%1 = alloca void (i64)*
  ;store void (i64)* @lambda_s, void (i64)** %1
  ;%2 = ptrtoint void (i64)** %1 to i64
  ;%f = call i64 @create_closure(i64 %2, i64 %n_1_x$0)

  ;f1 = get fun ptr(f)(get free vars(f), 1) 
  ;print get fun ptr(f1)(get free vars(f1), 3)
  ;%3 = call i64 @get_fun_ptr(i64 %f)



  ;%foo = alloca void (i64)*
  ;store void (i64)* @my_int_func, void (i64)** %foo
  ;%1 = load void (i64)** %foo
  ;call void %1(i64 2) 
  ret i32 0

}
