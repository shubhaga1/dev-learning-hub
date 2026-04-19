
public class InsertionSort {
    public static void main(String[] args) {
        int ar[] = {64, 34, 25, 12, 22, 11, 90};
        ar= insertionSort(ar);
        for(int i :ar){
            System.out.println(i);
        }
    }

    //  6,4,7,8,2,3
    /*

    * */
    public static int[] insertionSort(int[] ar){
        for(int i=0;i<ar.length-1;i++){
            int pass = ar[i];
            for(int j=0;j<pass;j++){
                if(ar[pass]<ar[j]){
                    int tem=ar[j+1];
                    ar[j+1]=ar[j];
                    ar[j]=tem;
                }
            }
        }
        return ar;
    }
}
