
document.addEventListener("DOMContentLoaded", function () {
    let firstNameInput = document.getElementById("id_first_name");
    let lastNameInput = document.getElementById("id_last_name");
    let usernameInput = document.getElementById("id_username");

    function updateUsername() {
        let firstName = firstNameInput.value.toLowerCase().trim();
        let lastName = lastNameInput.value.toLowerCase().trim();
        usernameInput.value = firstName && lastName ? `${firstName}_${lastName}` : "";
    }

    firstNameInput.addEventListener("input", updateUsername);
    lastNameInput.addEventListener("input", updateUsername);
});
