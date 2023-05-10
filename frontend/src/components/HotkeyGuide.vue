<template>
  <div>
    <v-menu offset-x>
      <template #activator="{ on, attrs }">
        <a v-bind="attrs" v-on="on" @click.stop>
          {{$t('Keyboard shortcuts')}}
        </a>
      </template>
      <div id="shortcut-guidelines">
        <ul>
          <li>
            {{$t('Annotation')}}:
            <ul>
              <li>
                {{$t('Ctrl + Alt + arrow up / down: set focus on next / previous annotation task')}}
              </li>
              <li>
                {{$t('arrow left / right: switch between labels inside the task currently in focus (blue border)')}}
              </li>
              <li>
                {{$t('Enter: select unselected (or select unselected) currently focused label (blue border) in currently focused task')}}
              </li>
              <li>
                {{$t('Ctrl + Enter: submit annotation(s) and go to the next document')}}
              </li>
            </ul>
          </li>
          <li>
            {{$t('Entities (text highlights). These shortcuts become available once you highlight some text (if an entity task is included in the project)')}}
            <ul>
              <li>{{$t('Enter: select currently focused label')}}</li>
              <li>{{$t('arrow / up: switch between labels')}}</li>
              <li>
                {{$t('arrow left / right: switch between tasks (only applicable if there are more than one entity tasks in the project)')}}
              </li>
            </ul>
          </li>
          <li>
            {{$t('Audio player')}}:
            <ul>
              <li>{{$t('Ctrl + space: play / pause')}}</li>
              <li>{{$t('Ctrl + arrow left / right: skip backward / forward')}}</li>
            </ul>
          </li>
        </ul>
      </div>
    </v-menu>
  </div>
</template>

<script>
export default {
  name: 'HotkeyGuide',
};
</script>

<style scoped>
#shortcut-guidelines {
  background: white;
  padding: 20px;
}
</style>
