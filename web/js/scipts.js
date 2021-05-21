var f = document.querySelector("form");
function connect() {
    n = document.querySelector("#u-name").value;
    p = document.querySelector("#p-word").value;
    
    if (n == '' || p == '') 
        alert("Failed : Username/Password is not given!!!");
    else {
        eel.login(n, p);
    }
}

eel.expose(verifiedLogin);
function verifiedLogin(msg = "See below for an example") {
    f.style.height = "350px";
    f.innerHTML = `

    <div class="but-ton">
        <div> 
        Use the following PHRASES while speaking.<br />
        <table>
            <thead>
                <th>Phrases</th>
                <th>Values</th>
            </head>
            <tbody>
                <tr>
                    <td>Asterisk</td>
                    <td>*</td>
                </tr>
                <tr>
                    <td>Open Bracket</td>
                    <td>(</td>
                </tr>
                <tr>
                    <td>Close Bracket</td>
                    <td>)</td>
                </tr>
                <tr>
                    <td>Character</td>
                    <td>Varchar2(25)</td>
                </tr>
                <tr>
                    <td>Equals</td>
                    <td>=</td>
                </tr>
                <tr>
                    <td>Not Equal to</td>
                    <td><></td>
                </tr>
                <tr>
                    <td>Describe</td>
                    <td>desc</td>
                </tr>
                <tr>
                    <td>Comma/And</td>
                    <td>,</td>
                </tr>
            </tbody>
        </table>                  
                    
        </div>
        <input type="button" id="lis-button" value="Listen" onclick="lisFunction()">
        <input type="button" id="close-button" value="Exit" onclick="closeFunction()">
        <p><b>${msg}<b></p>
    </div>
    
    `;

    if (document.querySelector(".extra-info").classList.contains("none-dis"))
        document.querySelector(".extra-info").classList.remove("none-dis");
}

eel.expose(ack);
function ack(msg = "Listening") {
    if (!f.classList.contains("f-box-shadow")) 
        f.classList.add("f-box-shadow");
    f.style.height = "80px";
    f.innerHTML = `

    <h1 class="lis-msg">${msg}...</h1>

    `; 
    if (msg == "Listening")
        if (document.querySelector(".extra-info").classList.contains("none-dis"))
            document.querySelector(".extra-info").classList.remove("none-dis");
}

eel.expose(process);
function process() {
    document.querySelector(".extra-info").classList.toggle("none-dis");
    f.classList.remove("f-box-shadow");
    f.innerHTML = `

    <h1 class="pro-msg">Processing</h1>

    `; 
}

eel.expose(response);
function response(data) {
    if (!f.classList.contains("f-box-shadow")) 
        f.classList.add("f-box-shadow");
    f.style.height = "300px";
    f.innerHTML = `

    <div class="edit">   
        <div class="menu">
            <input type="button" id="pre-button" value="<<" onclick=verifiedLogin() />
            <h1 class="span"> Edit </h1>
            <input type="button" id="lo-button" value="Log out" onclick="closeFunction()">
        </div>
        <textarea>${data}</textarea><br />
        <input type="button" id="run-button" value="Run" onclick="runFunction()">    
        <input type="button" id="lis-button" value="Listen" onclick="lisFunction()">
    <div>
    
    `;
}

eel.expose(closeit)
function closeit() {
    f.style.height = "300px";   
    f.innerHTML = `

    <h1> Database <br /> User Login</h1>
    <div class="user-name" >
        <input id="u-name" type="text" name="username" placeholder="Enter User name here">
        <input id="p-word" type="password" name="password" placeholder="Enter User Password here">
    </div>
    <div class="but-ton">
        <input type="button" value="Connect" onclick="connect()">
    </div>
    
    `;
    if (!document.querySelector(".extra-info").classList.contains("none-dis"))
        document.querySelector(".extra-info").classList.add("none-dis");
}

eel.expose(error)
function error() {
    alert("Login Failed : Username/Password is wrong");
}

function lisFunction() {
    eel.oracle_connection('');
}

function closeFunction() {
    eel.logout();
}

function runFunction() {
    eel.oracle_connection(document.querySelector("textarea").value);
}

eel.expose(startAlert);
function startAlert(errmsg) {
    verifiedLogin('last request : ' + errmsg);
}