const fs = require("fs")
const path = require("path")
const http = require("http")
const express = require("express")
const {Server} = require("socket.io")
const { exec } = require("child_process")

var app = express()
var server = http.createServer(app)
var io = new Server(server)

process.stdin.setEncoding("utf-8");

var intervals = {}

app.get("/", (req, res) => {
    res.sendFile(__dirname + "/index.html");
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

    socket.on("reqmem", () => {
        socket.emit("memory", socket.memory);
    });
});

server.listen(3000);

process.stdin.on("data", (data) => {
    let key = data.trim();
    switch(key) {
        case 'exit':
            process.exit();
        case 'sockets':
            console.log(Array.from(io.sockets.sockets.keys()).join("\n"));
            break;

        case '':
            break;
        default:
            console.log(key + " is not a command.");
            break;
    }
});

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
