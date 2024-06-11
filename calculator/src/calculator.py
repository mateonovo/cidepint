from src import operations


def calculate():
    num1 = float(input("Ingrese el primer numero"))
    num2 = float(input("Ingrese el segundo numero"))

    print("Suma: ", operations.add(num1,num2))
    print("Resta: ", operations.subtract(num1,num2))
    print("Multiplicacion: ", operations.multiply(num1, num2))
    print("División: ", operations.divide(num1, num2))
    