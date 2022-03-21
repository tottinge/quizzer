% rebase('skeleton.tpl', title=title)

% from dataclasses import asdict
<script src="//unpkg.com/json-form-custom-element"></script>
<script>
    document = "{{ asdict(quiz) }}";
</script>
<json-form name="title" schema=" " value={{ raw_quiz }}>
</json-form>

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
            <summary id="summary{{ id }}">{{ question.question }}</summary>
            <label for = "q{{ id }}-text">Question:</label>
            <input class="w3-input" id="q{{ id }}-text" type="text" value="{{ question.question }}">
        </details>
        % end
    </section>

</form>