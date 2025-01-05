export function DesignJson(jsonArray) {
    try {
        if (!Array.isArray(jsonArray) || !jsonArray.every(item => Array.isArray(item) && item.length === 2)) {
            throw new Error("Invalid input: Expected an array of [word, code] pairs.");
        }
        return jsonArray
            .map(([word, code]) => `${word.padEnd(10)} -> ${code}`)
            .join('\n');
    } catch (error) {
        return `Error: ${error.message}`;
    }
}