
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
  %4 = load i32 (i32)** %func
  %5 = call i32 %4(i32 5)
  ret i32 %5
}
