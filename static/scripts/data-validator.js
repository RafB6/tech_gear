//Check if username/password meets expectations.
formHandler = () => {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const error_msg = document.getElementById('Error_message');
    checkCookie(username, error_msg);
    
}

setCookie = (cname, cvalue, expDays) => {
    const d = new Date();
    d.setTime(d.getTime() + (expDays*24*60*60*1000));
    let expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/login; SameSite=Strict";
    console.log(getCookie(cname));
}

getCookie = (cname) => {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let carr = decodedCookie.split(";");
    for (let i = 0; i < carr.length; i++) {
        let c = carr[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

checkCookie = (usrnm,err) => {
    let Cusername = getCookie("username111");
    if (Cusername != "") {
        err.innerHTML = "Welcome back " + Cusername + "!";
    } else {
        if (usrnm != "" && usrnm != null) {
            setCookie("username111", usrnm, 1);
        }
    }
}
