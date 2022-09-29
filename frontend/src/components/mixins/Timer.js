export default {
    name: "Timer",
    props: {},
    data() {
        return {
            timer: '',
            time: 0, // total time spent annotating, excluding periods of inactivity
            t0: 0, // the start time of the current period of activity
            isInactive: false,
            inactivityTimeout: null,
            has_timing_started: false
        }
    },
    computed: {
        inactivity_timeout_duration() {
            if (this.batch.project) {
                return this.batch.project.timer_inactivity_threshold
            }
            return 10000
        },
    },
    methods: {
        startTiming: function () {
            if (this.has_timing_started) return
            this.has_timing_started = true
            this.activateActivityTracker();
            if(this.timer){
                clearInterval(this.timer)
            }
            this.time = 0
            this.initializeTimer()
        },
        initializeTimer(){
            this.t0 = this.getTime()
            this.timer = setInterval(this.updateTimer, 500)
            this.resetInactivityTimeout()
        },
        resetInactivityTimeout: function (){
            if (this.inactivityTimeout){
                clearTimeout(this.inactivityTimeout);
            }

            this.inactivityTimeout = setTimeout(() => {
                this.isInactive = true;
            }, this.inactivity_timeout_duration);
        },
        getTime(){
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
                    window.addEventListener(evt, this.respondToUserActivity);
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
}