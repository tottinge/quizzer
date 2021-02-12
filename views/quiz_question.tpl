% rebase('skeleton.tpl', title=title)
% include('sub_progress.tpl')

<form class="w3-container" action="/quizzes/{{quiz_name}}/{{question_number}}" method="POST">
    % from random import shuffle
    % choices = [*decoys,answer]
    % shuffle(choices)

    <section class="w3-card w3-container">
        <h3 class="w3-panel w3-teal w3-card-4 question-asked">{{question}}</h3>
        % for answer in choices:
        <div class="form-answer">
            <input type='radio' class="w3-radio" name='answer' id='{{answer}}' value='{{answer}}'/>
            <label for='{{answer}}'>
                {{answer}}
            </label>
        </div>
        % end
        <br/>
    </section>
    <br/>
    <button class="w3-btn w3-teal w3-round">Check Answer</button>
</form>

% if resources:
<div class="w3-panel">
<!--    w3-button w3-border w3-mobile-->
    <button class="w3-btn w3-round w3-light-gray" onclick="showResources()">Additional Resources</button>
    <section class="w3-hide w3-margin w3-ul w3-hoverable" id="resources">
        % for (text, url) in resources:
            <a class="w3-button w3-border w3-mobile" href="{{ url }}" target="_blank" rel="noreferrer noopener">{{ text }}</a>
        % end
    </section>
</div>
% end

<script>
    function showResources(){
        var resources = document.getElementById('resources');
        if (resources.className.includes("w3-show")) {
            resources.className = resources.className.replace(" w3-show", "")
        }else{
            resources.className += " w3-show"
        }
    }
</script>