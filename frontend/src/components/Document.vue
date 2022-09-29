<template>
  <div>
    <div v-if="document.document_sequence!=null">
      <h3>Document (id: {{ document.id }}): {{ increment(document.sequence_index) }}
        / {{ document.document_sequence.num_documents }}</h3>
    </div>
    <div v-else>
      <h3>Document (id: {{ document.id }})</h3>
    </div>

    <div id="doc">
      <div v-if="project.is_audio_annotated">
        <player
            :document="document"
            :enable-regions="true"
            @loaded="audio_loaded=true"
            v-model="annotated_regions"
            :region-tasks="region_tasks"
        />
      </div>
      <div id="text-container" v-if="project.is_text_annotated">
        <!--<span v-if="document.text" v-html="document.text"></span>-->
        <TextWithEntities
            :text="document.text"
            v-model="annotated_entities"
            :tasks="entity_tasks"
            :enabled="annotation_enabled"
        /><!--:labels="labels"-->

      </div>
    </div>
    <!--<div>
      annotated regs: {{annotated_regions}}
    </div>-->
  </div>
</template>
<script>
import Player from '@/components/Player'
import TextWithEntities from "@/components/TextWithEntities"
import {mapGetters} from 'vuex'


export default {
  name: "document",
  components: {
    Player,
    TextWithEntities,
  },
  data() {
    return {
      audio_loaded: false,
      /*annotated_regions: [],  // TODO: move to store
      region_tasks: [  // TODO: move to store
        {
          id: 1,
          name: "IVR",
          color: "lightblue",
        }
      ],*/
    }
  },
  created() {
    this.$store.commit('entities/RESET_ALL')
    this.$store.commit('regions/RESET_ALL')

  },
  computed: {
    ...mapGetters({
      entity_tasks: 'entities/entity_tasks',
      annotation_enabled: 'entities/annotation_enabled',
      region_tasks: 'regions/region_tasks',
      region_annotation_enabled: 'regions/annotation_enabled',
    }),
    annotated_regions: {
      get() {
        return this.$store.state.regions.annotated_regions
      },
      set(value) {
        this.$store.commit('regions/SET_ANNOTATED_REGIONS', value)
      }
    },
    annotated_entities: {
      get() {
        return this.$store.state.entities.annotated_entities
      },
      set(value) {
        this.$store.commit('entities/SET_ANNOTATED_ENTITIES', value)
      }
    },
    loaded() {
      if (this.project.is_audio_annotated) {
        return this.audio_loaded
      }
      return true
    }
  },
  props: {
    document: {
      type: Object,
      required: true,
    },
    project: {
      type: Object,
      required: true,
    },
  },
  methods: {
    increment(int) {
      return int + 1
    }
  },
  watch: {
    loaded() {
      if (this.loaded) this.$emit('loaded')
    },
    annotated_entities() {
      this.$store.commit('entities/SET_ANNOTATED_ENTITIES', this.annotated_entities)
    },
    annotated_regions() {
      this.$store.commit('regions/SET_ANNOTATED_REGIONS', this.annotated_regions)
    },
  },
}
</script>
<style>
#doc {
  margin-bottom: 20px;
}

#text-container {
  max-height: 500px;
  overflow-y: auto;
  padding-top: 15px;
}
</style>