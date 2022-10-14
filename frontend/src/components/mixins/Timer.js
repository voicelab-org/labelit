import {mapGetters} from 'vuex'

export default {
    name: "Timer",
    data() {
        return {
            timer: '',
            time: 0, // total time spent annotating, excluding periods of inactivity
            t0: 0, // the start time of the current period of activity
            isInactive: true,
            inactivityTimeout: null,
            has_timing_started: false,
            debounceTimeout: null,
        }
    },
    computed: {
        ...mapGetters({
            is_playing: 'player/isPlaying',
        }),
        inactivity_timeout_duration() {
            if(this.batch){
                if (this.batch.project) {
                    return this.batch.project.timer_inactivity_threshold
                }
            }
            return 10000
        },
    },
    created(){
        this.startTiming()
    },
    methods: {
        startTiming: function () {
            //if (this.has_timing_started) return
            this.has_timing_started = true
            this.activateActivityTracker();
            if (this.timer) {
                clearInterval(this.timer)
            }
            this.time = 0
            this.initializeTimer()
        },
        initializeTimer() {
            this.t0 = this.getTime()
            this.timer = setInterval(this.updateTimer, 500)
            this.resetInactivityTimeout()
        },
        resetInactivityTimeout: function () {
            if (this.inactivityTimeout) {
                clearTimeout(this.inactivityTimeout);
            }

            this.inactivityTimeout = setTimeout(() => {
                if (this.batch.project.does_audio_playing_count_as_activity) {
                    if (!this.is_playing) {
                        this.isInactive = true;
                    }
                    return
                }
                this.isInactive = true

            }, this.inactivity_timeout_duration);
        },
        getTime() {
            return new Date().getTime() // milliseconds
        },
        updateTimer: function () {
            if (!this.isInactive) {
                let now = this.getTime()
                this.time += now - this.t0
                this.t0 = now
            }
        },
        activateActivityTracker: function () {
            ["mousemove", "scroll", "keydown", "resize", "click"].forEach(
                (evt) => {
                    window.addEventListener(
                        evt,
                        () => {
                            // this.respondToUserActivity
                            // If there's a timer, cancel it
                            if (this.debounceTimeout) {
                                window.cancelAnimationFrame(this.debounceTimeout);
                            }

                            // Setup the new requestAnimationFrame()
                            this.debounceTimeout = window.requestAnimationFrame( () => {
                                // Run our scroll functions
                                this.respondToUserActivity()
                            });
                        },
                        false
                    );
                }
            )
        },
        respondToUserActivity: function () {
            if (this.isInactive) {
                this.isInactive = false;
                this.resetInactivityTimeout();
                this.initializeTimer()
            }
        },
    },
    watch: {
        is_playing() {
            this.resetInactivityTimeout()
        },
        numTasksSubmitted: {
            deep: true,
            handler(){
                this.startTiming()
            },
        },
    },
}