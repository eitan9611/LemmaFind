const express = require('express')

const router = express.Router();

const {SearchWord/*,DeleteWord_Hist,ReadWord_Hist*/} = require('../controllers/functions.js')

//------------------------------------------------------
//SEARCH  WORD: 
router.get('/:name',SearchWord)
//------------------------------------------------------
/*//READ WORD FROM HISTORY: 
router.get('/:id',ReadWord_Hist)
//-------------------------------------------------------
//DELETE WORD FROM HISTORY: 
router.delete('/:id',DeleteWord_Hist)
//--------------------------------------------------------------*/

module.exports = router;
