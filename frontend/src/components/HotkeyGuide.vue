<template>
  <div>

    <v-menu offset-x>
      <template v-slot:activator="{ on, attrs }">
        <a
            v-on="on"
            v-bind="attrs" @click.stop>Keyboard shortcuts</a>
      </template>
      <div id="shortcut-guidelines">
        <ul>
          <li>
            Annotation:
            <ul>
              <li>Ctrl + Alt + arrow up / down: set focus on next / previous annotation task</li>
              <li>arrow left / right: switch between labels inside the task currently in focus (blue border)</li>
              <li>Enter: select unselected (or select unselected) currently focused label (blue border) in currently focused task</li>
              <li>Ctrl + Enter: submit annotation(s) and go to the next document</li>
            </ul>
          </li>
          <li>
            Entities (text highlights).
            These shortcuts become available once you highlight some text (supposing an entity task is in the project)
            <ul>
              <li>Enter: select currently focused label</li>
              <li>arrow / up: switch between labels</li>
              <li>arrow left / right: switch between tasks (only applicable if there are more than one entity tasks in the project)</li>
            </ul>
          </li>
          <li>
            Audio player:
            <ul>
              <li>Ctrl + space: play / pause</li>
              <li>Ctrl + arrow left / right: skip backward / forward</li>
            </ul>
          </li>
        </ul>
      </div>
    </v-menu>
  </div>
</template>

<script>
export default {
  name: "HotkeyGuide",
}
</script>

<style scoped>

#shortcut-guidelines {
  background: white;
  padding: 20px;
}

</style>