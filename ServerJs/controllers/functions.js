const axios = require('axios'); // הספרייה לשליחת בקשות HTTP

//INPUT: word
//OUTPUT: json that has all the words in the bank that has the same root as word 
//function that sends a request to Flask API
const runPythonScript = (word) => {
    return new Promise((resolve, reject) => {
        // URL ל-API של Flask שמריץ את ה-main
        const pythonAPIUrl = 'http://python:5000/run-main'; // python:5000 אם אתה עובד בתוך Docker

        // שולח בקשה ל-API של Flask
        axios.post(pythonAPIUrl, { word: word })
            .then(response => {
                resolve(response.data); // מחזיר את התוצאה שקיבלתם מ-Flask
            })
            .catch(error => {
                console.log("Error calling Python API:", error);
                reject("Error calling Python API: " + error.message);
            });
    });
};

const SearchWord = async (req, res) => {
    try {
        const name = req.params.name;
        const pythonResult = await runPythonScript(name);

        let result;
        try {
            result = pythonResult; // התוצאה כבר במבנה JSON, אין צורך לפרס אותה שוב
        } catch (parseError) {
            throw new Error("Failed to parse Python script output to JSON");
        }

        res.status(200).json(result);
        console.log("we did it!")
    } catch (err) {
        res.status(500).json({ message: err.message + " #failed to search" });
    }
};

//ההערה ארוכה ששמרנו
/*
const ReadWord_Hist = async (req,res) => { //everything that comes after ":" is acceptable by the server
    try {
        const written_id = req.params.id;
        const specific_word = await Word.findByIdAndDelete(written_id,req.body);
        if(!specific_word)
            return res.status(404).json({message:"we didnt found the requested word to delete"})
        res.status(200).json({ message: "word "+ written_id +" has deleted successfully!" });
    } catch (err){
        res.status(500).json({message: err.message})
    }
} 
const DeleteWord_Hist = async (req,res) => {
    try {
        const words = await Word.find({}) //nothing here becuase I want all words
        res.status(200).json(words)
    } catch (err){
        res.status(500).json({message: err.message})
    }
}
*/

module.exports = {
    SearchWord/*,
    ReadWord_Hist,
    DeleteWord_Hist*/
};
