/**
 * POC 3: Regex Frustration Detector
 *
 * The article claimed Claude monitors prompts for frustration keywords using regex.
 * This is REAL — AI systems do log/flag user frustration for product improvement.
 * It's basic but effective.
 *
 * Run: node detector.js
 */

// Frustration patterns — ordered from mild to severe
const FRUSTRATION_PATTERNS = [
    // Mild frustration
    { regex: /\b(not working|doesn't work|isn't working|won't work)\b/i,    level: 1, label: "mild" },
    { regex: /\b(why (is|does|won't|can't)|what the)\b/i,                  level: 1, label: "mild" },
    { regex: /\b(still (not|wrong|broken|failing))\b/i,                    level: 1, label: "mild" },

    // Moderate frustration
    { regex: /\b(again|same (error|issue|problem)|keeps (failing|breaking))\b/i, level: 2, label: "moderate" },
    { regex: /\b(useless|waste of time|broken|terrible|awful)\b/i,         level: 2, label: "moderate" },
    { regex: /\b(i (already|told you|said|mentioned))\b/i,                 level: 2, label: "moderate" },

    // High frustration
    { regex: /\b(wtf|what the (hell|heck|f\*ck)|are you (kidding|serious))\b/i, level: 3, label: "high" },
    { regex: /\b(completely (wrong|broken|useless|stupid))\b/i,            level: 3, label: "high" },
    { regex: /\b(give up|forget it|this is hopeless|you('re| are) (useless|terrible|awful))\b/i, level: 3, label: "high" },

    // Abandonment signals
    { regex: /\b(forget (it|this|everything)|never mind|cancel|stop)\b/i,  level: 4, label: "abandonment" },
    { regex: /\b(switching to (gpt|gemini|copilot|chatgpt))\b/i,           level: 4, label: "abandonment" },
];

function detectFrustration(message) {
    const matches = [];
    let maxLevel = 0;

    for (const pattern of FRUSTRATION_PATTERNS) {
        const match = message.match(pattern.regex);
        if (match) {
            matches.push({ matched: match[0], level: pattern.level, label: pattern.label });
            maxLevel = Math.max(maxLevel, pattern.level);
        }
    }

    return {
        frustrated: matches.length > 0,
        level: maxLevel,
        label: maxLevel === 0 ? "none" : matches.find(m => m.level === maxLevel).label,
        matches,
        // What Claude logs internally
        logEvent: matches.length > 0 ? {
            timestamp: new Date().toISOString(),
            frustrationLevel: maxLevel,
            triggers: matches.map(m => m.matched),
            message: message.substring(0, 100)   // truncated for privacy
        } : null
    };
}

// Test prompts — ranging from calm to frustrated
const testMessages = [
    "Can you help me fix this function?",
    "This is not working, I keep getting the same error",
    "Why does this keep failing? I already told you the array is empty",
    "This is completely useless wtf, same broken output again",
    "Forget it, I'm switching to ChatGPT",
];

console.log("=".repeat(65));
console.log("Regex Frustration Detector — like Claude monitors prompts");
console.log("=".repeat(65));

testMessages.forEach(msg => {
    const result = detectFrustration(msg);
    const icon = ["😊", "😐", "😤", "😡", "💀"][result.level] || "😊";
    console.log(`\n${icon} Input: "${msg}"`);
    console.log(`   Frustrated: ${result.frustrated}`);
    console.log(`   Level:      ${result.level} (${result.label})`);
    if (result.matches.length > 0) {
        console.log(`   Triggers:   ${result.matches.map(m => `"${m.matched}"`).join(", ")}`);
        console.log(`   Log event:  ${JSON.stringify(result.logEvent)}`);
    }
});

console.log("\n" + "=".repeat(65));
console.log("Key insight from the article:");
console.log("=".repeat(65));
console.log("Claude does NOT change behavior based on this detector.");
console.log("It only LOGS the event for product analytics.");
console.log("'Advanced emotional intelligence' = just regex keyword matching.");
