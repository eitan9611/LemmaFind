// this routes brings us what we made in "routes". 
// IMPORTANT! in the start of the path- ".." = jump twice above / "." = jump once TO RELATIVE FOLDER (in this case into "PEROOSHPROJ")
const express = require('express')
//const mongoose = require('mongoose')
const path = require('path');
//require("dotenv").config();

const PersonalPage = require("./routes/PersonalPage.js")
//-------------------------------------------------------------------------------------------
const app = express()
//-------------------------------------------------------------------------------------------
//middlewares:
app.use(express.json());
app.use(express.urlencoded({extended: false}))//to handle with URL and not just json
app.use(express.static('public'));
//-------------------------------------------------------------------------------------------
/*//mongoDB_connection: 
const dbUser = process.env.DB_USER;
const dbPassword = process.env.DB_PASSWORD;
const dbCluster = process.env.DB_CLUSTER;
const dbName = process.env.DB_NAME;
const appName = process.env.DB_APPNAME;
mongoose.connect(
    "mongodb+srv://" + dbUser + ":" + dbPassword + "@" + dbCluster + "/" + dbName + "?retryWrites=true&w=majority&appName=" + appName,
)
.then(() => {
    console.log("connected to database!");
})
.catch(err => {
    console.log("connection failed!\n" + err);
});*/
//-----------------------------------------------------------------
//Routes:
app.get('/', (req, res) => {    // get = excatly "/" , not for subpaths
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});
app.use("/api/PersonalPage",PersonalPage) //use = subpaths too.
//---------------------------------------------------------------------------------------------
app.listen(3000, () => {
    console.log("this server is running on port 3000")
})