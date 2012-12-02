;Program([SLambda([], StmtList([VarAssign('1_callfunctmp', CallFunc(Name(inject_int), [Const(3)])), VarAssign('2_callfunctmp', CallFunc(Name(print_any), [Name(1_callfunctmp)])), Return(Const(0))]), main)])

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

; Definition of main function
define i32 @main() {

       %1 = call i64 @inject_int(i64 3)
       call void @print_any(i64 %1)
       ret i32 0

}
