var f = document.querySelector("form");
function connect() {
    n = document.querySelector("#u-name").value;
    p = document.querySelector("#p-word").value;
    
    if (n == '' || p == '') 
        alert("Fields left Empty!!!");
    else {
        eel.login(n, p);
    }
}

eel.expose(verifiedLogin);
function verifiedLogin(msg) {
    f.style.height = "300px";
    f.innerHTML = `

    <div class="but-ton">
        <div> 
        Use the following PHRASES for the values while speaking.<br />
        <table>
            <thead>
                <th>Phrases</th>
                <th>values</th>
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
                    <td>Varchar2()</td>
                </tr>
                <tr>
                    <td>Equals</td>
                    <td>=</td>
                </tr>
            </tbody>
        </table>
        </div>
        <input type="button" id="lis-button" value="Listen" onclick="lisFunction()">
        <input type="button" id="close-button" value="Exit" onclick="closeFunction()">
        <p><b>${msg}<b></p>
    </div>

    `;
}

eel.expose(listen);
function listen() {
    f.style.height = "80px";
    f.innerHTML = `

    <h1>Listening...<input type='button' id="back-button" value="Stop" onclick="killFunction()"></h1>

    `; 
}

eel.expose(response);
function response(data) {
    f.style.height = "350px";
    f.innerHTML = `
    <div class="edit">
    <h1>Edit</h1>
    <textarea>${data}</textarea><br />
    <input type="button" id="run-button" value="Run" onclick="runFunction()">    
    <input type="button" id="lis-button" value="Listen" onclick="lisFunction()">    
    <br />
    <input type="button" id="close-button" value="Exit" onclick="closeFunction()">
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
}

eel.expose(error)
function error() {
    alert("Login error : Username/Password is wrong");
}

function lisFunction() {
    eel.oracle_connection('');
}

function closeFunction() {
    eel.logout();
}

function killFunction() {
    eel.kill();
}

function runFunction() {
    eel.oracle_connection(document.querySelector("textarea").value);
}

eel.expose(startAlert);
function startAlert(msg, err) {
    verifiedLogin('Your last request Failed :' + msg);
}