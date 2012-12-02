; PRINT FUNCTIONS
; void print_int_nl(int x);
declare void @print_int_nl(i32 %x)
; void print_any(pyobj p);

; INPUT FUNCTIONS
; int input();
declare i32 @input()
; pyobj input_int();
declare i32 @input_int()

;int is_true(pyobj v);
;int tag(pyobj val);

;int is_int(pyobj val);
;int is_bool(pyobj val);
;int is_big(pyobj val);
;int is_function(pyobj val);
;int is_object(pyobj val);
;int is_class(pyobj val);
;int is_unbound_method(pyobj val);
;int is_bound_method(pyobj val);

;pyobj inject_int(int i);
;pyobj inject_bool(int b);
;pyobj inject_big(big_pyobj* p);

;int project_int(pyobj val);
;int project_bool(pyobj val);
;big_pyobj* project_big(pyobj val);

;big_pyobj* create_list(pyobj length);
;big_pyobj* create_dict();
;pyobj set_subscript(pyobj c, pyobj key, pyobj val);
;pyobj get_subscript(pyobj c, pyobj key);

;big_pyobj* add(big_pyobj* a, big_pyobj* b);
;int equal(big_pyobj* a, big_pyobj* b);
;int not_equal(big_pyobj* x, big_pyobj* y);

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

;pyobj error_pyobj(char* string);
