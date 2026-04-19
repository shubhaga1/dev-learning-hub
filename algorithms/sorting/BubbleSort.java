
public class BubbleSort {
    public static void main(String[] args) {
        int ar[] = {64, 34, 25, 12, 22, 11, 90};
        ar= bubbleSort(ar);
        for(int i :ar){
            System.out.println(i);
        }
    }

    //  6,4,7,8,2,3
    /*  46723]678

    * */
    public static int[] bubbleSort(int[] ar){
        for(int i=0;i<ar.length-1;i++){
            for(int j=0;j<ar.length-i-1;j++){
                if(ar[j]>ar[j+1]){
                    int tem=ar[j+1];
                    ar[j+1]=ar[j];
                    ar[j]=tem;
                }
            }
        }
        return ar;
    }
}
