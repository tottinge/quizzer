<!DOCTYPE html>
<html>
<head>
    <title>{{title}}</title>
</head>

<body>
<section>
    <h1 id="title" class="page-title">{{title}}</h1>

    % if correct:
    <p>Your answer <em>"{{selection}}"</em> is correct.</p>
    <p>Fact is successfully acquired and recalled. You're on your way...</p>
        % if next_url:
        <a href={{next_url}} id="next_question">Next Question</a>
        % else:
        <p>You have completed this quiz! Yay you!</p>
        <a href="/" id="go_home">Rock On</a>
        % end

    % else:
    <p>Your answer <em>"{{selection}}"</em> is not what we're looking for.</p>
    <a href="{{return_url}}" id="try_again">Try Again</a>
    % end
</section>

</body>

</html>
