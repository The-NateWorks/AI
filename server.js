const fs = require("fs")
const path = require("path")
const http = require("http")
const express = require("express")
const {Server} = require("socket.io")
const { exec } = require("child_process")

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
    socket.memory = {};
    socket.history = [];

    socket.on("you", (mess) => {
        socket.history.push("You: " + mess);
        exec(`python server.py "${mess}" "${JSON.stringify(socket.memory).replaceAll("\"", "'")}"`, (err, stout, stderr) => {
            if (err) {
                console.log(err)
                process.exit()
            }
            let memory = parseJSON(stout);
            socket.memory = JSON.parse(memory);
            let response = stout.replace(memory, "");
            socket.history.push("Nautical: " + response);
            socket.emit("nautical", response);
        });
    });

    socket.on("reqhis", () => {
        socket.emit("history", socket.history);
    });
});

server.listen(3000)

function parseJSON(string) {
    let levels = 1;
    let firstBracket = string.indexOf("{");
    for (let i = firstBracket + 1; i < string.length; i++) {
        if (string[i] == "{") {
            levels += 1;
        } else if (string[i] == "}") {
            levels -= 1;
        }
        if (levels == 0) {
            return string.slice(firstBracket, i + 1);
        }
    }
    return null
}
