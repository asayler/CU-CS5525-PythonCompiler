; PRINT FUNCTIONS
; void print_int_nl(int x);
declare i64 @print_int_nl(i64)
; void print_any(pyobj p);
declare i64 @print_any(i64)

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
declare i64 @inject_big(i64)

; INJECT
;int project_int(pyobj val);
declare i64 @project_int(i64)
;int project_bool(pyobj val);
declare i64 @project_bool(i64)
;big_pyobj* project_big(pyobj val);
declare i64 @project_big(i64)

; UTILITIES
;int is_true(pyobj v);
declare i64 @is_true(i64)
;int tag(pyobj val);
declare i64 @tag(i64)
;pyobj error_pyobj(char* string);
declare i64 @error_pyobj();

; IS_*
;int is_int(pyobj val);
declare i64 @is_int(i64);
;int is_bool(pyobj val);
declare i64 @is_bool(i64);
;int is_big(pyobj val);
declare i64 @is_big(i64);
;int is_function(pyobj val);
declare i64 @is_function(i64);
;int is_object(pyobj val);
declare i64 @is_object(i64);
;int is_class(pyobj val);
declare i64 @is_class(i64);
;int is_unbound_method(pyobj val);
declare i64 @is_unbound_method(i64);
;int is_bound_method(pyobj val);
declare i64 @is_bound_method(i64);

;big_pyobj* create_list(pyobj length);
declare i64 @create_list(i64);
;big_pyobj* create_dict();
declare i64 @create_dict();
;pyobj set_subscript(pyobj c, pyobj key, pyobj val);
declare i64 @set_subscript(i64, i64, i64);
;pyobj get_subscript(pyobj c, pyobj key);
declare i64 @get_subscript(i64, i64);

;big_pyobj* add(big_pyobj* a, big_pyobj* b);
declare i64 @add(i64, i64);
;int equal(big_pyobj* a, big_pyobj* b);
declare i64 @equal(i64, i64);
;int not_equal(big_pyobj* x, big_pyobj* y);
declare i64 @not_equal(i64, i64);

;big_pyobj* create_closure(void* fun_ptr, pyobj free_vars);
declare i64 @create_closure(i64, i64);
;void* get_fun_ptr(pyobj);
declare i64 @get_fun_ptr(i64);
;pyobj get_free_vars(pyobj);
declare i64 @get_free_vars(i64);
;big_pyobj* set_free_vars(big_pyobj* b, pyobj free_vars);
declare i64 @set_free_vars(i64, i64);

;big_pyobj* create_class(pyobj bases);
;big_pyobj* create_object(pyobj cl);
;int inherits(pyobj c1, pyobj c2);
;big_pyobj* get_class(pyobj o);
;big_pyobj* get_receiver(pyobj o);
;big_pyobj* get_function(pyobj o);
;int has_attr(pyobj o, char* attr);
;pyobj get_attr(pyobj c, char* attr);
;pyobj set_attr(pyobj obj, char* attr, pyobj val);
