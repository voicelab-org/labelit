<template>
    <div id="blue-filter">
        <div id="blue-filter-controls">
            <v-icon :color="'orange'">mdi-weather-night</v-icon>
            <span>{{slider}} %</span>
            <v-slider
              v-model="slider"
              :color="'orange'"
              :track-color="'blue'"
            ></v-slider>
        </div>
        <div id="blue-filter-overlay" :style="overlayStyle"></div>
    </div>
</template>

<script>

import LocalStorageService from '@/services/local.storage.service.js'

export default {
    name: "BlueFilter",
    data(){
        return {
            slider: 45,
        }
    },
    created(){
        if (LocalStorageService.getBlueFilterValue() == null) {
            LocalStorageService.setBlueFilterValue(this.slider)
        }
        this.slider = LocalStorageService.getBlueFilterValue()
    },
    computed: {
        overlayStyle(){
            return {
                background: 'rgba(255, 255, 0, ' + this.slider / 100 + ')'
            }
        },
    },
    watch: {
        slider(){
            LocalStorageService.setBlueFilterValue(this.slider)
        },
    },
}

</script>

<style lang="scss">
    #blue-filter{
        #blue-filter-controls {
            margin-right: 10px;
            min-width: 150px;
            display: flex;
            align-items: center;
            > .v-input {
                max-height: 30px;
            }

            > .v-icon {
                margin-right: 5px;
            }
        }
    }

    #blue-filter-overlay {
        position: fixed;
        background-blend-mode: multiply;
        //background-color: rgba(255, 255, 0, 0.5);
        pointer-events: none;
        opacity: 0.5;
        min-height: 100vh;
        width: 100%;
        z-index: 200000;
        top: 0;
        left: 0;
        height: 100vh;
    }
</style>