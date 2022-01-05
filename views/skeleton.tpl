<!DOCTYPE html>
<html lang="en">
<head>
    <title>{{ title }}</title>
    <link href="https://www.w3schools.com/w3css/4/w3.css" rel="stylesheet"/>
    <meta content="width=device-width, initial-scale=1" name="viewport"/>

</head>

<body>
<header>
    <h1 class="page-title " id="title">
        <a href="/" id="return_link">
            <img align="left"
                 hspace="5"
                 src="/favicon.ico"
                 style="height:1.1em;"
                 alt="The quizzology logo as a link to the home page"
            />
        </a>
        {{title}}
    </h1>
    <p>Hi, <span id="user_name">default text</span>, you <span id="user_role">default role</span></p>
</header>

    <script>
        function get_cookie(name_of_cookie) {
            const desired = document.cookie.split(';').filter(function (x) {
                    const [name, _] = x.split('=');
                    return name.trim() === name_of_cookie
                }
            ).pop()
            const [_, value] = desired.split('=');
            const trimmed = value.replace(/"/g, '')
            return trimmed
        }

        document.getElementById('user_name').innerText = get_cookie('qz-user-name');
        document.getElementById('user_role').innerText = get_cookie('qz-user-role');
    </script>

{{!base}}

</body>
</html>
