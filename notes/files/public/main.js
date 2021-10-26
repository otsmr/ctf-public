
document.querySelector("button").addEventListener("click",  () => {
    
    const note = document.querySelector('[name=note]').value;
    const title = document.querySelector('[name=title]').value;
    
    if (title === "" || note === "")
        return;
    
    fetch("/note/create", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            note: DOMPurify.sanitize(note),
            title: title.match(/([A-Za-z0-9])/g).join("").slice(0, 20)
        })
    }).then(e => {
        location.reload();
    })
    
});

function reportNote (noteid) {

    const element = document.querySelector(".noteid-" + noteid + " button");
    element.innerHTML = "Bitte warten...";
    element.style.borderColor = "green";

    fetch("/note/report/" + noteid)
    .then(e => e.json())
    .then(e => {
        element.remove();
        if (e.error)
            return alert("Unbekannter Fehler");
        alert(e.message);
    })

    return false;

}

window.onload = () => {

    const notesParentEl = document.querySelector(".notes");

    for (const note of notes) {

        const noteEl = document.createElement("div");
        noteEl.className = "note noteid-" + note.id;

        noteEl.innerHTML = `
<p class="username">${note.title}</p>
<p>${DOMPurify.sanitize(note.note)}</p>
<button onclick="reportNote('${note.id}')">Anzeigefehler melden</button>`;

        notesParentEl.append(noteEl);

    }

}