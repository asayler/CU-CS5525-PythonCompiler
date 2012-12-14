define i64 @main() {
    $x = call i64 @input_int()
    $y = $x
    ret i64 $y
}
