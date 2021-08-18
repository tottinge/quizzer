% rebase('skeleton.tpl', title=title)


<section>
    <h2 class="w3-teal w3-panel">Quizzes Available:</h2>
    <div class="w3-container w3-ul w3-hoverable">
        % for (name, description, filename) in choices:
        <a class="quiz_selection w3-button w3-border w3-mobile w3-cell" href="/study/{{name}}">
            {{ description }}
        </a>
        % end
    </div>
</section>

