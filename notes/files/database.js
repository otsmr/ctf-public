const fs = require("fs");
const path = require("path");

module.exports = class SessionDatabase {

    constructor () {

        this._sessionid = null;
        this._dbFile = path.join(__dirname, "notes.json");

        if (!fs.existsSync(this._dbFile))
            fs.writeFileSync(this._dbFile, "{}");
        else
            this._removeOldSessions();

    }

    get isAdmin () {
        return this._getData()[this._sessionid].isAdmin;
    }

    updateCurrentSessionToAdmin () {

        const data = this._getData();
        data[this._sessionid].isAdmin = true;
        this._updateData(data);

    }

    getNotes (sessionid = this._sessionid) {

        if (sessionid === null)
            return false;

        const data = this._getData();

        return data[sessionid].notes;

    }

    addNote (note) {

        if (this._sessionid === null)
            return false;

        const data = this._getData();

        data[this._sessionid].notes.push(note);

        this._updateData(data);

        return true;

    }

    isSessionValid (uuidv4) {

        const data = this._getData();

        if (
            typeof uuidv4 === "undefined" ||
            uuidv4.indexOf("-4") === -1 ||
            data[uuidv4] === undefined
        ) {
            return false;
        }

        if (data[uuidv4].expire < +new Date()) {
            
            delete data[uuidv4];
            this._updateData(data);
            return false;

        }

        return true;

    }

    getNewSessionIfNotValid (uuidv4) {

        if (!this.isSessionValid(uuidv4)) {
            return this._createNewSession();
        }

        return null;

    }

    initSession (uuidv4) {
        this._sessionid = uuidv4;
    }

    _removeOldSessions () {

        const data = this._getData();

        for (const uuid in data) {
            if (data[uuid].expire < +new Date()) {
                delete data[uuid];
            }
        }

        this._updateData(data);

    }

    getUuidv4 () {

        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });

    }

    _updateData (data) {

        try {
            fs.writeFileSync(this._dbFile, JSON.stringify(data));
        } catch (error) {
        }

    }

    _getData () {
        try {
            return JSON.parse(fs.readFileSync(this._dbFile))
        } catch (error) {
            return {}
        }
    }

    _createNewSession () {

        const data = this._getData();
        const uuid = this.getUuidv4();

        data[uuid] = {
            expire: +new Date() + 1000 * 60 * 60 * 24, // one day 
            isAdmin: false,
            notes: [{
                id: this.getUuidv4(),
                note: "Hallo Welt, dass hier ist eine weitere Notizen-App, die sogar der Admin verwendet :^)",
                title: "Einfache Notizen-App"
            }]
        }

        this._updateData(data);

        return uuid;

    }
    
}