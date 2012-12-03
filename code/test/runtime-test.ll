; Note: this test is expected to fail at runtime on a bad assert
; It is just an example of pyobj and bigpyobj use

declare i64 @input_int()
declare void @print_any(i64)
declare i8* @project_big(i64)
declare i64 @inject_big(i8*)

define i32 @main() {
  %po = alloca i64, align 8
  %bpo = alloca i8*, align 8
  %1 = call i64 @input_int()
  store i64 %1, i64* %po, align 8
  %2 = load i64* %po, align 8
  call void @print_any(i64 %2)
  %3 = load i64* %po, align 8
  %4 = call i8* @project_big(i64 %3)
  store i8* %4, i8** %bpo, align 8
  %5 = load i8** %bpo, align 8
  %6 = call i64 @inject_big(i8* %5)
  store i64 %6, i64* %po, align 8
  ret i32 0
}
