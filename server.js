const fs = require("fs")
const path = require("path")
const http = require("http")
const express = require("express")
const {Server} = require("socket.io")
const { exec } = require("child_process")
const { parseArgs } = require("util")
const { createClient } = require("@supabase/supabase-js");

var app = express()
var server = http.createServer(app)
var io = new Server(server)

process.stdin.setEncoding("utf-8");
var client = createClient("https://jgjdxlulszliepzrhgff.supabase.co", "sb_publishable_JUr3sNI84pNyl30pzxD-dA_bvZhy1w3");

var intervals = {}

app.get("/", (req, res) => {
    res.sendFile(__dirname + "/index.html");
});

app.get("/admin", (req, res) => {
    res.sendFile(path.resolve("./admin.html"))
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

server.listen(3000, () => {
    setInterval(async () => {
        let data = await client.from("events").select("*").eq("program", "nautical");
        data.data.forEach(async dati => {
            for (c in dati.data.server.commands) {
                let split = dati.data.server.commands[c];
                dati.data.server.commands.splice(c, 1);
                await client.from("events").update({data: dati.data}).eq("program", "nautical");
                cmds(split[0], split.slice(1));
            }
        });
    }, 500);
});

process.stdin.on("data", (data) => {
    let key = data.trim();
    let cmd = key.split(" ")[0];
    let args = key.split(" ").slice(1);
    cmds(cmd, args);
});

function cmds(cmd, args) {
    switch(cmd) {
        case 'exit':
            process.exit();
        case 'sockets':
            console.log(Array.from(io.sockets.sockets.keys()).join("\n"));
            break;
        case 'alertAll':
            if (args[0]) {
                io.emit("alert", args[0]);
            }

        case '':
            break;
        default:
            console.log(cmd + " is not a command.");
            break;
    }
}

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
