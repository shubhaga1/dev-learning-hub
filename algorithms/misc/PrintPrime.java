

import java.util.Scanner;

class PrintPrime {

    public static void main(String[] args) {
        System.out.println("Enter the number till which you want to list all prime numbers");
        int num;
        try (Scanner sc = new Scanner(System.in)) {
            num = sc.nextInt();
        }
        System.out.println("Prime number between 0 and " + num + " are ");
        printAllPrimeNo(num);
        //printPrime(num);
    }

    static void printAllPrimeNo(int n) {
        for (int i = 0; i < n; i++) {
            if (i == 0 || i == 1) {
                continue;
            }
            printPrime(i);
        }
    }

    static void printPrime(int num) {
        int flag = 1;
        for (int j = 2; j <= num / 2; j++) {
            if (num % j == 0) {
                flag = 0;
                break;
            }
        }
        if (flag == 1) {
            System.out.print(num+",");
        }
    }
}
