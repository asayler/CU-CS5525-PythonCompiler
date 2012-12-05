; PRINT FUNCTIONS
; void print_int_nl(int x);
declare i32 @print_int_nl(i32)
; void print_any(pyobj p);
declare i32 @print_any(i32)

; INPUT FUNCTIONS
; int input();
declare i32 @input()
; pyobj input_int();
declare i32 @input_int()

; PROJECT
; pyobj inject_int(int i);
declare i32 @inject_int(i32)
; pyobj inject_bool(int b);
declare i32 @inject_bool(i32)
; pyobj inject_big(big_pyobj* p);
declare i32 @inject_big(i32)

; INJECT
;int project_int(pyobj val);
declare i32 @project_int(i32)
;int project_bool(pyobj val);
declare i32 @project_bool(i32)
;big_pyobj* project_big(pyobj val);
declare i32 @project_big(i32)

; UTILITIES
;int is_true(pyobj v);
declare i32 @is_true(i32)
;int tag(pyobj val);
declare i32 @tag(i32)
;pyobj error_pyobj(char* string);
declare i32 @error_pyobj();

; IS_*
;int is_int(pyobj val);
declare i32 @is_int(i32);
;int is_bool(pyobj val);
declare i32 @is_bool(i32);
;int is_big(pyobj val);
declare i32 @is_big(i32);
;int is_function(pyobj val);
declare i32 @is_function(i32);
;int is_object(pyobj val);
declare i32 @is_object(i32);
;int is_class(pyobj val);
declare i32 @is_class(i32);
;int is_unbound_method(pyobj val);
declare i32 @is_unbound_method(i32);
;int is_bound_method(pyobj val);
declare i32 @is_bound_method(i32);

;big_pyobj* create_list(pyobj length);
declare i32 @create_list(i32);
;big_pyobj* create_dict();
declare i32 @create_dict();
;pyobj set_subscript(pyobj c, pyobj key, pyobj val);
declare i32 @set_subscript(i32, i32, i32);
;pyobj get_subscript(pyobj c, pyobj key);
declare i32 @get_subscript(i32, i32);

;big_pyobj* add(big_pyobj* a, big_pyobj* b);
declare i32 @add(i32, i32);
;int equal(big_pyobj* a, big_pyobj* b);
declare i32 @equal(i32, i32);
;int not_equal(big_pyobj* x, big_pyobj* y);
declare i32 @not_equal(i32, i32);

;big_pyobj* create_closure(void* fun_ptr, pyobj free_vars);
;void* get_fun_ptr(pyobj);
;pyobj get_free_vars(pyobj);
;big_pyobj* set_free_vars(big_pyobj* b, pyobj free_vars);

;big_pyobj* create_class(pyobj bases);
;big_pyobj* create_object(pyobj cl);
;int inherits(pyobj c1, pyobj c2);
;big_pyobj* get_class(pyobj o);
;big_pyobj* get_receiver(pyobj o);
;big_pyobj* get_function(pyobj o);
;int has_attr(pyobj o, char* attr);
;pyobj get_attr(pyobj c, char* attr);
;pyobj set_attr(pyobj obj, char* attr, pyobj val);
