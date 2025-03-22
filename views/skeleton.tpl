<!DOCTYPE html>
<html lang="en">
<head>
    <title>{{ title }}</title>
    <link href="https://www.w3schools.com/w3css/4/w3.css" rel="stylesheet"/>
    <link href="/static/quizzology.css" rel="stylesheet"/>

    <meta content="width=device-width, initial-scale=1" name="viewport"/>

</head>

<body>
<header class="w3-display-container">
    <h1 class="page-title" id="title">
        <a href="/" id="return_link">
            <img src="/favicon.ico"
                 class="w3-btn"
                 style="height: 1.1em; vertical-align: top; padding: 0;"
                 alt="The quizzology logo as a link to the home page"
            /></a>
        {{title}}
    </h1>
    <a class="w3-display-right w3-button w3-blue-gray" href="/login">
        <span id="nav-user-name" >default text</span> (<span id="nav-user-role">default role</span>)
    </a>
</header>

    <script>
        function get_cookie(name_of_cookie) {
            const desired = document.cookie.split(';').filter(function (x) {
                    const [name, _] = x.split('=');
                    return name.trim() === name_of_cookie
                }
            ).pop()
            if(desired){
                const [_, value] = desired.split('=');
                return value.replace(/"/g, '')
            }
        }

        document.getElementById('nav-user-name').innerText = get_cookie('qz-user-name');
        document.getElementById('nav-user-role').innerText = get_cookie('qz-user-role');
    </script>

{{!base}}

</body>
</html>
