<template>
    <div>
            <div v-if="document.document_sequence!=null">
                <h3>Document (id: {{document.id}}): {{increment(document.sequence_index)}}
                / {{document.document_sequence.num_documents}}</h3>
            </div>
            <div v-else>
                <h3>Document (id: {{document.id}})</h3>
            </div>
            
            <div id="doc">
                <div v-if="project.is_audio_annotated">
                    <player :document="document" @loaded="audio_loaded=true" />
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
    </div>
</template>
<script>
import Player from '@/components/Player'
import TextWithEntities from "@/components/TextWithEntities"
import { mapGetters } from 'vuex'


export default {
    name: "document",
    components : {
        Player,
        TextWithEntities,
    },
    data(){
        return {
            audio_loaded: false,
        }
    },
    created(){
        this.$store.commit('entities/RESET_ALL')

    },
    computed: {
        ...mapGetters({
          entity_tasks : 'entities/entity_tasks',
          annotation_enabled: 'entities/annotation_enabled',
        }),
        annotated_entities: {
          get () {
            return this.$store.state.entities.annotated_entities
          },
          set (value) {
            this.$store.commit('entities/SET_ANNOTATED_ENTITIES', value)
          }
        },
        loaded(){
            if (this.project.is_audio_annotated) {
                return this.audio_loaded
            }
            this.$emit('loaded')
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
        increment(int){
            return int + 1
        }
    },
    watch: {
        loaded(){
            if (this.loaded) this.$emit('loaded')
        },
        annotated_entities(){
          this.$store.commit('entities/SET_ANNOTATED_ENTITIES', this.annotated_entities)
        },
    },
}
</script>
<style>
#doc{
    margin-bottom: 20px;
}

#text-container{
    max-height: 500px;
    overflow-y: auto;
    padding-top: 15px;
}
</style>