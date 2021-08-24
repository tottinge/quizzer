<section class="w3-panel">
    <label for="progress">Progress: {{question_number+1}} of {{quiz.number_of_questions()}} </label>
    <progress id="progress" max="{{quiz.number_of_questions()}}" value="{{question_number+1}}"></progress>
</section>