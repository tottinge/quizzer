% rebase('skeleton.tpl', title=title)
% include('sub_progress.tpl')
<section class="w3-panel">
    % if correct:
        <div id="confirmation" class="w3-pale-green w3-container">
            <p>Your Answer <em>{{selection}}</em> is correct</p>
            <p>{{confirmation}}</p>
        </div>
        % if next_url:
            <a class="w3-btn w3-teal w3-round" href={{next_url}} id="next_question">Next Question</a>
        % else:
            <p>You have completed this quiz!</p>
            %if incorrect_answers == 0:
                <p>You answered perfectly. Well done, you!</p>
            %else:
                <p>You answered incorrectly only {{incorrect_answers}} times.</p>
            %end
            <a class="w3-btn w3-teal w3-round" href="/" id="go_home">Rock On</a>
        % end
    % else:
        <p class="w3-container w3-pale-red">Your answer <em>"{{selection}}"</em> is not what we're looking for.</p>
        <a class="w3-btn w3-teal w3-round" href="{{return_url}}" id="try_again">Try Again</a>
    % end
</section>

