const fs = require("fs")
const path = require("path")
const http = require("http")
const express = require("express")
const {Server} = require("socket.io")
const { exec } = require("child_process")
const { stderr } = require("process")

var app = express()
var server = http.createServer(app)
var io = new Server(server)

var intervals = {}

app.get("/", (req, res) => {
    res.sendFile(__dirname + "/index.html");
});

app.get("/evts", (req, res) => {
    res.send(fs.readFileSync(__dirname + "/evts.json", "utf8"))
});

io.on("connection", (socket) => {
    console.log("User connected: " + socket.id);

    socket.on("you", (mess) => {
        exec("python server.py " + mess, (err, stout, stderr) => {
            socket.emit("nautical", stout);
        });
    });
});

server.listen(3000)

function getEvents() {
    return JSON.parse(fs.readFileSync(path.join(__dirname, "evts.json"), "utf8"));
}
function setEvents(events) {
    fs.writeFileSync(path.join(__dirname, "evts.json"), JSON.stringify(events));
}