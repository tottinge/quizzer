% rebase('skeleton.tpl', title=title)


<section>
    <h2 class="w3-teal w3-panel">Quizzes Available:</h2>
    <div class="w3-container w3-hoverable">
        % for (name, description, filename) in choices:
        <a class="quiz_selection" href="/study/{{name}}">
            <section class="w3-panel w3-card w3-third w3-hover-shadow quiz-card" >
                <div>
                    <img class="quiz-icon" src="/static/favicon.ico">
                <p class="w3-center w3-large">{{ description }}</p>
                </div>
            </section>
        </a>

        % end
    </div>
</section>

