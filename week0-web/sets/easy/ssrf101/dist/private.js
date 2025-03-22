const express = require('express')
const app = express()
const private2Port = 10011

app.get('/flag', (req, res) => {
    res.sendFile(__dirname + '/flag.txt')
})

// this port is only exposed locally
app.listen(private2Port, () => {
    console.log(`Listening on ${private2Port}`)
})