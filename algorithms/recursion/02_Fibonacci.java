
import java.util.Scanner;

class Fibonacci {
    public static int fibonacci(int n) {
        if (n <= 1) {
            return n;
        }
        
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
    
    public static int getNumber(){
        try(Scanner scanner = new Scanner(System.in)){
            System.out.println("Enter the number till which you need Fibonacci Series");
            return (scanner.nextInt());
        }
    }

    public static void main(String[] args) {
        int n = getNumber();
        System.out.println("Fibonacci sequence up to " + n + ":");
        for (int i = 0; i <= n; i++) {
            System.out.print(fibonacci(i) + " ");
        }
    }
}
// Fibonacci sequence up to 10:
// 0 1 1 2 3 5 8 13 21 34 55
