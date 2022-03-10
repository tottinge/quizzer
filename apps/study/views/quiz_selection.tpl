% rebase('skeleton.tpl', title=title)


<section>
    <h2 class="w3-teal w3-panel">Quizzes Available:</h2>
    <div class="w3-container w3-hoverable">
        % for (name, description, filename) in choices:
        <a class="quiz_selection w3-container w3-card w3-third w3-hover-shadown quiz-card" href="/study/{{name}}">
                <p class="w3-container w3-center">
                    <img class="quiz-icon" src="/static/favicon.ico">
                </p>
                <footer class="w3-center w3-container w3-teal w3-large">{{ description }}</footer>
        </a>

        % end
    </div>
</section>

