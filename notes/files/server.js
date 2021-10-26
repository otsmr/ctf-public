
const express = require('express');
const puppeteer = require('puppeteer');
const cookieParser = require('cookie-parser');
const SessionDatabase = require("./database");
const fs = require("fs");
const path = require("path");

const app = express();
const port = 9001;

app.use(cookieParser())
app.use(express.json());

app.use((req, res, next) => {

    const db = new SessionDatabase();
    let uuid = null;

    if ((uuid = db.getNewSessionIfNotValid(req.cookies.session)) !== null) {
        res.cookie('session', uuid, {
            httpOnly: true
        });
    } else {
        uuid = req.cookies.session;
    }

    db.initSession(uuid);
    
    req.sessionID = uuid;
    req.db = db;

    next();

})

app.post("/note/create", (req, res, next) => {

    const note = {
        id: req.db.getUuidv4(),
        note: req.body.note.slice(0, 1000),
        title: req.body.title.match(/([A-Za-z0-9])/g).join("").slice(0, 20)
    }

    req.db.addNote(note);

    res.send(JSON.stringify({
        id: note.id
    }))

})

app.get("/", (req, res, next) => {

    let htmlContent = fs.readFileSync(path.join(__dirname, "html/index.html")).toString();

    let notes = req.db.getNotes();

    if (req.db.isAdmin) {
        notes = [
            {
                id: req.db.getUuidv4(),
                text: "flag_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX_",
                title: "Flag:^)"
            }
        ]
    }

    res.send(htmlContent.replace("{{notes}}", JSON.stringify(notes)));

})

app.get("/admin/:sessionid/:noteid", (req, res, next) => {

    const localhost = [
        "::1",
        "localhost",
        "127.0.0.1",
        "::ffff:127.0.0.1"
    ]

    if (localhost.indexOf(req.connection.remoteAddress) === -1) {
        console.log("only localhost allowed!", req.connection.remoteAddress);
        return res.send("only localhost allowed");
    }

    if (!req.db.isSessionValid(req.params.sessionid)) {
        return res.send("session not valid");
    }

    req.db.updateCurrentSessionToAdmin();

    const note = req.db.getNotes(req.params.sessionid).find(e => e.id === req.params.noteid);

    if (!note)
        return res.send("note not found");

    let htmlContent = fs.readFileSync(path.join(__dirname, "html/index.html")).toString();

    res.send(htmlContent.replace("{{notes}}", JSON.stringify([note])));

})

app.get("/note/report/:noteid", async (req, res, next) => {

    const note = req.db.getNotes().find(e => e.id === req.params.noteid);

    if (!note)
        return res.send(JSON.stringify({
            error: true
        }));

    const browser = await puppeteer.launch({
        args: [ "--no-sandbox" ], // FIXME?: remove --no-sandbox
        headless: true
    });

    const page = await browser.newPage();

    setTimeout(async () => {
        // Timeout for the browser, because it needs a lot of resources
        try {
            await browser.close();
        } catch (error) { }

    }, 4000);

    try {

        await page.goto('http://localhost:9001/admin/' + req.sessionID + "/" + note.id, {
            waitUntil: "networkidle0"
        });
    
        await browser.close();
        
    } catch (error) {

        console.log("browser timeout");
        
    }


    res.send(JSON.stringify({
        error: false,
        message: "Der Admin konnte kein Problem finden!"
    }));

})

app.use(express.static(__dirname + '/public'));

app.listen(port, () => {
    console.log(`listening at http://localhost:${port}`)
})