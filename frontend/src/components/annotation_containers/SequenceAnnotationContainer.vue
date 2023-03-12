<template>
  <div>
    <v-menu
        transition="slide-x-transition"
        right
        offset-x
        nudge-left="19px"
        @input="step = 1"
      >
        <template #activator="{ on: menu, attrs }">
          <v-tooltip
            content-class="bv-module-tooltip"
            transition="slide-x-transition"
            right
            nudge-left="18"
          >
            <template #activator="{ on: tooltip }">
              <div v-on="{ ...tooltip, ...menu }">
                <v-btn
                  v-bind="attrs"
                  icon
                  color="mediumgrey"
                  height="40"
                  width="70"
                >
                  <v-icon>mdi-school</v-icon>
                </v-btn>
              </div>
            </template>
            <span>Batvoice Academy</span>
          </v-tooltip>
        </template>
        <v-card>
          <div class="bv-section">
            <p class="bolder">Accédez à la Batvoice Academy</p>
            <p>
              Familiarisez-vous avec BatvoiceAI, revoyez les bases ou explorez
              de nouvelles fonctionnalités.
            </p>
            <v-stepper v-model="step">
              <v-stepper-header>
                <v-stepper-step :complete="step > 1" step="1">
                  {{ $t('copyPassword') }}
                </v-stepper-step>

                <v-divider></v-divider>

                <v-stepper-step :complete="step > 2" step="2">
                  {{ $t('goToAcademy') }}
                </v-stepper-step>
              </v-stepper-header>

              <v-stepper-items>
                <v-stepper-content step="1">
                  <v-card
                    class="mb-12 d-flex flex-column align-center justify-center"
                    height="200px"
                  >
                    <p>
                      La Batvoice Academy est sécurisée par un mot de passe
                      différent de votre mot de passe utilisateur
                    </p>
                    <p>Copiez-le en appuyant sur le bouton ci-dessous</p>
                    <v-btn
                      large
                      color="primary"
                      @click.stop="
                        step = 2;
                      "
                    >
                      {{ $t('copyPassword') }}
                      <v-icon right dark> mdi-content-copy </v-icon>
                    </v-btn>
                  </v-card>
                </v-stepper-content>

                <v-stepper-content step="2">
                  <v-card
                    class="mb-12 d-flex flex-column align-center justify-center"
                    height="200px"
                  >
                    <p>Le mot de passe a été ajouté à votre presse-papiers.</p>
                    <p>
                      Si la Batvoice Academy vous demande un mot de passe, vous
                      pouvez le coller dans le champs prévu
                      <br />
                      avec Ctrl + C ou clic-droit > coller
                    </p>
                    <v-btn
                      large
                      color="primary"
                      @click.stop="
                        step = 2;
                      "
                    >
                      {{ $t('goToAcademy') }}
                    </v-btn>
                  </v-card>
                </v-stepper-content>
              </v-stepper-items>
            </v-stepper>
          </div>
        </v-card>
      </v-menu>
    <div v-if="annotations" id="annotation-forms-t">
      <div
          v-for="(annotation, i) in annotations"
          :key="annotation.id"
          :class="getAnnotationClasses(annotation, i == focus_index)"
      >
        <component
            :is="getFormForTask(getTaskForAnnotation(annotation))"
            :annotation="annotation"
            :time="time"
            :task="getTaskForAnnotation(annotation)"
            :submitting="submitting"
            :review-mode="reviewMode"
            :document="document"
            :focused="i == focus_index"
            @submitted="$emit('submitted')"
            @submiterror="$emit('submiterror')"
            @focus="focus_index = i"
        />
        <div v-if="annotation.qa_invalidation_comment">
          {{ annotation.qa_invalidation_comment }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import AnnotationContainer from './mixins/AnnotationContainer'

export default {
  name: "ListAnnotationContainer",
  mixins: [
    AnnotationContainer,
  ],
  props: {
    annotations: {
      type: Array,
      required: true,
    },
    tasks: {
      type: Array,
      required: true,
    },
    time: {
      type: Number,
    },
    submitting: {
      type: Boolean,
      required: true,
    },
    reviewMode: {
      type: Boolean,
    },
  },
  data() {
    return {
      focus_index: 0,
    }
  },
  methods: {
    browseTasks(direction) {
      if (direction == 'right') {
        if (this.focus_index == this.annotations.length - 1) {
          this.focus_index = 0;
        } else {
          this.focus_index++;
        }
      }

      if (direction == 'left') {
        if (this.focus_index == 0) {
          this.focus_index = this.annotations.length - 1;
        } else {
          this.focus_index--;
        }
      }
    },
  }
}
</script>

<style scoped>

</style>