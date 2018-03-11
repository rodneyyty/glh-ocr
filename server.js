const path = require('path')
const express = require('express')
const app = express()
const bodyParser = require('body-parser')
app.use('/data', express.static('data/Demo Library'))
app.get('/datas.json', (req, res) => {
  res.sendFile(path.join(__dirname + '/vis/datas.json'))
})
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname + '/vis/index.html'))
});
app.listen(3000)
