const axios = require('axios'); // allows to send HTTP requests

//INPUT: word
//OUTPUT: json that has all the words in the bank that has the same root as word 
//function that sends a request to Flask API
const runPythonScript = (word) => {
    return new Promise((resolve, reject) => {

        const pythonAPIUrl = 'http://python:5000/run-main'; // to go to port 5000 and there ask our specific python function. 

        // POST REQ - and attached json that contains the word to search. 
        axios.post(pythonAPIUrl, { word: word })
            .then(response => {
                resolve(response.data); 
            })
            .catch(error => {
                console.log("Error calling Python API:", error);
                reject("Error calling Python API: " + error.message);
            });
    });
};

const SearchWord = async (req, res) => {
    try {
        const word = req.params.word_to_search; //getting the end of the url as a parameter
        const pythonResult = await runPythonScript(word); // getting the json from the POST req

        try {
        } catch (parseError) {
            throw new Error("Failed to parse Python script output to JSON");
        }
        res.status(200).json(pythonResult);
    } catch (err) {
        res.status(500).json({ message: err.message + " #failed to search" });
    }
};

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
