% rebase('skeleton.tpl', title=title)

<form id="quiz_edit" action="/edit" method="POST">
    <label for="quiz_name">Name</label>
    <input type="text" id="quiz_name" name="name" value="{{ quiz.name }}">

    <label for="quiz_title">Title</label>
    <input type="text" id="quiz_title" name="title" value="{{ quiz.title }}">

    <button id="save_changes" type="submit">Save</button>

    <section id="questions">
        <div>QUESTIONS</div>
        % for (id,question) in enumerate(quiz.questions):
        <details id="{{ id }}">
            <summary>{{ question.question }}</summary>
        </details>
        % end
    </section>
</form>