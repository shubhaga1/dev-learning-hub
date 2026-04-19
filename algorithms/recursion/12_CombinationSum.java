import java.util.ArrayList;
import java.util.List;

// https://leetcode.com/problems/combination-sum/description/
// Find all combinations from candidates[] that sum to target (reuse allowed)
// Approach: pick or skip each element, backtrack when target exhausted

class CombinationSum {

    static void combination(int[] candidates, int target, int index,
                            List<Integer> current, List<List<Integer>> result) {
        if (index == candidates.length) {
            if (target == 0) result.add(new ArrayList<>(current));  // valid combination found
            return;
        }

        if (candidates[index] <= target) {
            current.add(candidates[index]);
            combination(candidates, target - candidates[index], index, current, result);  // pick same again
            current.remove(current.size() - 1);  // backtrack
        }

        combination(candidates, target, index + 1, current, result);  // skip current element
    }

    static List<List<Integer>> combinationSum(int[] candidates, int target) {
        List<List<Integer>> result = new ArrayList<>();
        combination(candidates, target, 0, new ArrayList<>(), result);
        return result;
    }

    public static void main(String[] args) {
        int[] candidates = {2, 3, 6, 7};
        int target = 7;
        System.out.println("Combinations summing to " + target + ": "
                           + combinationSum(candidates, target));  // [[2,2,3],[7]]
    }
}
