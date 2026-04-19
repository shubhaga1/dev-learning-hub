
import java.util.Scanner;

class LinearSearch {
    public static void main(String[] args) {
        int ar[] ={6,4,7,8,2,3};
        int find;
        try (Scanner sc = new Scanner(System.in)) {
            find = sc.nextInt();
        }

        for(int i=0;i<ar.length;i++){
            if(find==ar[i]){
                System.out.println("number is available in the array at"+ i +" position");
            }
        }
    }
}
