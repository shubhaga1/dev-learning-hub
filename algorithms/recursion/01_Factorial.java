
import java.util.InputMismatchException;
import java.util.Scanner;

class Factorial {
    
    public static void main(String[] args) {
        try {
            getNumber();
        } catch (InputMismatchException ex) {
            System.out.println(" an Integer is required");
           // s.nextLine();
            getNumber();
        }

    }

    public static void getNumber(){
        try (Scanner s = new Scanner(System.in)) {   // try-with-resources: auto-closes s
            System.out.println("Find me the factorial of ?");
            int num = s.nextInt();
            System.out.println((factorial(num)));
        }
    }

    public static long factorial(int n) {
        // Base condition
        if (n <= 0)
            return 1;
        return n * factorial(n - 1);
    }
}
