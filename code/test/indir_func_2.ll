; PRINT FUNCTIONS
; void print_int_nl(int x);
declare void @print_int_nl(i64)
; void print_any(pyobj p);
declare void @print_any(i64)

; INPUT FUNCTIONS
; int input();
declare i64 @input()
; pyobj input_int();
declare i64 @input_int()

; PROJECT
; pyobj inject_int(int i);
declare i64 @inject_int(i64)
; pyobj inject_bool(int b);
declare i64 @inject_bool(i64)
; pyobj inject_big(big_pyobj* p);
declare i64 @inject_big(i8*)

; INJECT
;int project_int(pyobj val);
declare i64 @project_int(i64)
;int project_bool(pyobj val);
declare i64 @project_bool(i64)
;big_pyobj* project_big(pyobj val);
declare i8* @project_big(i64)

define void @my_int_func(i64 %x){

  call void (i64)* @print_int_nl(i64 %x)
  ret void

}

; Definition of main function
define i32 @main() {

  %foo = alloca void (i64)*
  store void (i64)* @my_int_func, void (i64)** %foo
  %1 = load void (i64)** %foo
  call void %1(i64 2) 
  ret i32 0

}
