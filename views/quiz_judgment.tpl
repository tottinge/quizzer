<!DOCTYPE html>
<html>
<head>
    <title>{{title}}</title>
</head>

<body>
<section>
    <h1 id="title" class="page-title">{{title}}</h1>
    <p>{{text}}</p>
    % if not correct:
    <a href="{{url}}">Try Again</a>
    % end
</section>

</body>

</html>
