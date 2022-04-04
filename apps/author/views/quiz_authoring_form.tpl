% rebase('skeleton.tpl', title=title)

% from dataclasses import asdict
<script src="//unpkg.com/json-form-custom-element"></script>
<script>
    document = "{{ asdict(quiz) }}";
</script>

<form id="quiz_edit" action="/author/edit" method="POST">

    <input type="hidden" id="quiz" name="quiz" value="{'updated':'false'}">

    <json-form name="charlie" schema="{{ schema }}" value="{{ raw_quiz }}"
            onChange="changeDocumentValue(this)"
    ></json-form>

    <script>
        function changeDocumentValue(origin) {
            const documentField = document.getElementById("quiz");
            const value = origin.getAttribute("value");
            documentField.value = value;
        }
    </script>

    <button id="save_changes" type="submit">Save</button>

    <json-form name="tryme" value="{{ try_me_input }}" schema="{{ try_me_schema }}">

    </json-form>

</form>