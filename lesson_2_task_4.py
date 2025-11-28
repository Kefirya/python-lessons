def fizz_buzz (n):
    for m in range(1, n+1):
        if m % 5 == 0 and m % 3 == 0:
            print ("FizzBuzz")
        elif m % 3 == 0:
            print("Fizz")
        elif m % 5 == 0:
            print("Buzz")

n = int(input("Введите число: "))
fizz_buzz(n)
