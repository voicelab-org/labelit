export default {
    name: "Timer",
    props: {},
    data() {
        return {
            timer: '',
            time: 0,
            isInactive: false,
            throttlerTimeout: null,
            inactivityTimeout: null,
            THROTTLER_TIMEOUT_DURATION: 2000,
        }
    },
    computed: {
        INACTIVITY_TIMEOUT_DURATION() {
            if (this.batch.project) {
                return this.batch.project.timer_inactivity_threshold
            }
            return 10000
        },
    },
    methods: {
        startTimer: function () {
            this.activateActivityTracker();
            clearInterval(this.timer)
            this.time = 0
            this.timer = setInterval(this.updateTimer, 1000)
        },
        updateTimer: function () {
            if (!this.isInactive) {
                this.time += 1000
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
            }

            if (!this.throttlerTimeout) {
                this.throttlerTimeout = setTimeout(() => {
                    this.resetInactivityTimeout();
                    clearTimeout(this.throttlerTimeout);
                    this.throttlerTimeout = null;
                }, this.THROTTLER_TIMEOUT_DURATION);
            }
        },
        resetInactivityTimeout: function () {
            clearTimeout(this.inactivityTimeout);

            this.inactivityTimeout = setTimeout(() => {
                this.respondToUserActivity();
                this.isInactive = true;
                this.time = 0
                clearInterval(this.timer)
                this.timer = setInterval(this.updateTimer, 1000)
            }, this.INACTIVITY_TIMEOUT_DURATION);
        },
    },
}