define i64 @main() {
    l_1_block:
        %0 = call i64 @input_int()
        %1 = call i64 @is_true(i64 %0)
        switch i64 0, label %l_2_test [  ]
    l_2_test:
        switch i64 %1, label %l_3_else [  i64 1, label %l_3_then  ]
    l_3_then:
         %2 = call i64 @inject_int(i64 3)
         switch i64 0, label %l_5_end [  ]
    l_4_else:
         %3 = call i64 @inject_int(i64 9)
         switch i64 0, label %l_5_end [  ]
    l_5_end:
         $4 = phi i64 [ %2, %l_3_then ], [ %3, %l_4_else ]
         switch i64 0, label %l_6_block [  ]
    l_6_block:
         ret i64 $4
}
