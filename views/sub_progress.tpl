<section class="w3-panel">
    <label for="progress">Progress: {{question_number+1}} of {{quiz.number_of_questions()}} </label>
    <progress id="progress" value="{{question_number+1}}" max="{{quiz.number_of_questions()}}"></progress>
</section>