% rebase('skeleton.tpl', title=title)


<section>
<h2 class="w3-teal">Quizzes Available:</h2>
<div class="w3-container w3-row">
% for (name, description, filename) in choices:
    <a class="quiz_selection w3-col s9 w3-container" href="/quizzes/{{name}}/0">
        {{ description }}
    </a>
% end
</div>
</section>

