var oldSeconds;

function editClicked() {
    $("#saveEditButton").show();
    $("#cancelEditButton").show();
    $("#editButton").hide();

    var secondsField = $("#seconds")[0];
    secondsField.disabled = false;
    oldSeconds = secondsField.value;
    secondsField.focus();
}

function cancelClicked() {
    $("#saveEditButton").hide();
    $("#cancelEditButton").hide();
    $("#editButton").show()

    var secondsField = $("#seconds")[0];
    secondsField.disabled = true;
    secondsField.value = oldSeconds;    
}

function saveClicked() {
    var secondsField = $("#seconds")[0];
    window.location.href = "/updateTimer?seconds=" + secondsField.value;
}
