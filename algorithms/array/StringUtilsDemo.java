/**
 * String Manipulation Demo
 *
 * Common string operations: prefix check, replace, substring by index.
 *
 * Input:  "/content/amazon/us/en/articles/learning/june-2020-release/june-2020-release-v1.2.pdf"
 * Output: "us/en"  // strip prefix, take segment after first slash
 *
 * Approach: Standard Java String methods — startsWith, replace, indexOf, substring
 * Time: O(n)  Space: O(n)
 */
class StringUtilsDemo {
    public static void main(String[] args) {
        String url = "/content/amazon/us/en/articles/learning/june-2020-release/june-2020-release-v1.2.pdf";
        System.out.println("Input:  " + url);
        System.out.println("Output: " + extractSegment(url));
    }

    private static String extractSegment(String url) {
        String prefix = "/content/amazon/";
        if (url.startsWith(prefix)) {
            url = url.replace(prefix, "");
        }
        int indexOfSlash = url.indexOf('/');
        if (indexOfSlash >= 0 && indexOfSlash + 1 < url.length()) {
            url = url.substring(indexOfSlash + 1, indexOfSlash + 6);
        }
        return url;
    }
}
