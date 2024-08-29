function validation() {
    // Fetching values from input fields
    let name = document.getElementById("nameValue").value.trim();
    let email = document.getElementById("emailValue").value.trim();
    let password = document.getElementById("passwordValue").value.trim();
    
    // Regular expression for validating email format
    let emailRegex = /^[^\s@]+@gmail\.com$/;

    // Clearing previous error messages
    document.getElementById("v1").innerHTML = "";
    document.getElementById("v2").innerHTML = "";
    // document.getElementById("v3").innerHTML = "";
    document.getElementById("v4").innerHTML = "";

    // Validation for name field
if (name === "") {
    document.getElementById("v1").innerHTML = "! Please fill in your name";
    return false;
}

// Validation for name field to contain only numbers
if (!/^[a-zA-Z\s]+$/.test(name)) {
    document.getElementById("v1").innerHTML = "Please enter name only in the number field.";
    document.getElementById("nameValue").value = "";
    return false;
}
 

    // Validation for name field to contain only letters
    // if (!/^[a-zA-Z\s]+$/.test(name)) {
    //     document.getElementById("downalert1").innerHTML = "! Name must contain only letters";
    //     return false;
    // }

    // Validation for email field
    if (email === "") {
        document.getElementById("v2").innerHTML = "! Please fill in your email";
        return false;
    }

    // Validation for email field format
    if (!emailRegex.test(email)) {
        document.getElementById("v2").innerHTML = "! Please enter a valid Gmail address";
        return false;
    }

    // Validation for phone number field


    // Validation for phone number field length
    
    // Validation for password field
    // Validation for password field length
    // Validation for password field
if (password === "") {
    document.getElementById("v4").innerHTML = "! Please fill in your password";
    return false;
}

// Validation for password field length
let varsize = 5; 
if (password.length !== varsize) {
    document.getElementById("v4").innerHTML = "! Password must be 5 characters long";
    return false;
}


// All validations pass, return true
return true;
}
function loginvalidation() {
    let email = document.getElementById("emailVal").value.trim();
    let password = document.getElementById("passwordVal").value.trim();

    let emailRegex = /^[^\s@]+@gmail\.com$/;

    document.getElementById("firstIN").innerHTML = "";
    document.getElementById("secondIN").innerHTML = "";

    if (email === "") {
        document.getElementById("firstIN").innerHTML = "! Please fill in your email";
        return false;
    }

    if (!emailRegex.test(email)) {
        document.getElementById("firstIN").innerHTML = "! Please enter a valid Gmail address";
        return false;
    }

    // Validation for password field
    if (password === "") {
        document.getElementById("secondIN").innerHTML = "! Please fill in your password";
        return false;
    }

    // Validation for password field length
    let varsize = 5; 
    if (password.length !== varsize) {
        document.getElementById("secondIN").innerHTML = "! Password must be 5 characters long";
        return false;
    } else if (password.length > varsize) {
        document.getElementById("secondIN").innerHTML = "! Password must be at least 5 characters long";
        document.getElementById("nameValue").value = "";
        return false;
    }

    // All validations pass, return true
    return true;
}
