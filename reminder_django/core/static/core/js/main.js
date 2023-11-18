if (user != 'AnonymousUser') {
    setInterval(() => {
        getActiveReminders()
    }, 10000);
}


function getActiveReminders() {

    fetch("/get_reminders/", {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
        })
        .then((response) => response.json()) // returns a promise object
        .catch((error) => console.log('Error: ' + error))
        .then(data => inspectReminders(data));
}


function deactivateReminder(pk) {

    console.log('deactivating reminder nr: ', pk);

    var url = '/bin_old_reminder/'
    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'pk': pk })
        })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            // location.reload();
            console.log(data);
        });
}


function reminderMessage(pk) {
    console.log('alert View for reminder nr: ', pk);

    var url = '/message/';
    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'pk': pk })
        })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            console.log(data);
        });

}


function temporaryAlert(message, duration) {
    var boxMessage = document.createElement("div");
    boxMessage.setAttribute("id", "alert-box");
    boxMessage.innerHTML = message;
    document.body.appendChild(boxMessage);
    setTimeout(function() {
        boxMessage.parentNode.removeChild(boxMessage);
    }, duration);
    setTimeout(function() {
        location.reload();
    }, duration);
}


function playAudio() {
    document.getElementById('soundToPlay').play();
}


function inspectReminders(data) {
    let alertTime = 0;
    for (let reminder of data) {
        const text = reminder.fields.text;
        const date = reminder.fields.date;
        const repeat = reminder.fields.repeat;

        const epochCurrentTime = Date.now();
        const reminderAlarm = new Date(date);
        var zoneOffset = new Date().getTimezoneOffset();
        const epochReminderTime = reminderAlarm.getTime() + zoneOffset * 60 * 1000;
        const epochRepeat = repeat * 1000

        if ((epochCurrentTime + 10000) > epochReminderTime) {

            if (epochRepeat == 0) {
                alertTime = 9000;
                const pk = reminder.pk;
                deactivateReminder(pk);

            } else {
                const timeDifference = epochCurrentTime + 10000 - epochReminderTime;
                if (timeDifference < epochRepeat) {
                    alertTime = timeDifference;
                } else {
                    alertTime = timeDifference % epochRepeat;
                }
            }

            if (alertTime < 10000) {
                playAudio();
                responsiveVoice.speak(text);
                temporaryAlert(text, 10000);
                reminderMessage(reminder.pk);
            }
        }
    }
    console.log('looking for alerts in ...', data.length, 'active reminders');
}