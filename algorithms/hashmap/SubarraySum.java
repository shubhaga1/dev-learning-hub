import java.util.HashMap;

class Solution {
    public int subarraySum(int[] nums, int k) {
        int sum =0;
        int ans =0;
        HashMap<Integer, Integer> map = new HashMap<>();
       // map.put(0,1);
        for (int j=0;j<nums.length;j++){
            sum+= nums[j];
            if(map.containsKey(sum-k)){
                ans+= map.get(sum-k);
            }
            map.put(sum,map.getOrDefault(sum,0)+1);
        }
        return ans;
    }
}

// https://leetcode.com/problems/subarray-sum-equals-k/description/
/*

Approach
This code is an implementation of a solution to find the number of contiguous subarrays in an array of integers that add up to a target sum, k.

The approach used in this solution is to use a HashMap, map, to store the cumulative sum of the elements in the array and the number of times that cumulative sum has been seen so far. The cumulative sum of the elements in a subarray can be represented as the difference between the cumulative sum of the elements in the array up to the end of the subarray and the cumulative sum of the elements in the array up to the start of the subarray.

The function starts by initializing a variable sum to keep track of the cumulative sum of the elements in the array, and a variable ans to keep track of the number of subarrays that add up to k. The function also adds an entry to map with key 0 and value 1, which represents the cumulative sum of an empty subarray, which is 0.

The function then iterates over each element in the array, adding the current element to the cumulative sum, and checking if the cumulative sum minus k is in map. If it is, the function adds the value of that key in map to the count of subarrays that add up to k, as that represents the number of times that cumulative sum has been seen so far, and therefore the number of subarrays that end at the current element and add up to k.

Finally, the function adds the current cumulative sum to map, with a value of 1 if it is the first time that cumulative sum has been seen, or increments the value of that key by 1 if it has been seen before.

Complexity
Time complexity:
The time complexity of this solution is O(n), where n is the length of the array. This is because, in the worst case, all elements in the array need to be processed once, so the number of operations is proportional to the length of the array.

Space complexity:
The space complexity of this solution is O(n), as in the worst case, all elements in the array can have different cumulative sums, so the HashMap can store at most n entries.

*/
