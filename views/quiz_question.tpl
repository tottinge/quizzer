% rebase('skeleton.tpl', title=quiz.title)
% include('sub_progress.tpl')

<form class="w3-container" action="/quizzes/{{quiz.name}}/{{question_number}}" method="POST">
    % from random import shuffle
    % choices = [*question.decoys,question.answer]
    % shuffle(choices)

    <section class="w3-card w3-container">
        <h3 class="w3-panel w3-teal w3-card-4 question-asked">{{question.question}}</h3>
        % for choice in choices:
        <div class="form-choice">
            <input type='radio' class="w3-radio" name='answer' id='{{choice}}' value='{{choice}}'/>
            <label for='{{choice}}'>
                {{choice}}
            </label>
        </div>
        % end
        <br/>
    </section>
    <br/>
    <button class="w3-btn w3-teal w3-round" id="submit_answer">Check Answer</button>
</form>

% if question.resources:
<div class="w3-panel w3-dropdown-hover">
    <button class="w3-button w3-round w3-light-gray">Additional Resources</button>
    <section class="w3-dropdown-content w3-bar-block w3-border" id="resources">
        % for (text, url) in question.resources:
            <a class="w3-button w3-bar-item"
               href="{{ url }}"
               target="_blank"
               rel="noreferrer noopener">{{ text }}
            </a>
        % end
    </section>
</div>
% end
