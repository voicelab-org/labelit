<template>
  <div>
    <div class="stream-waveforms" @click="waveFormClicked" >
      <div class="stream-waveforms-cursor" ref="cursor"></div>
      <div class="stream-waveforms-bars"></div>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3v4";

export default {
  name: "StreamWaveForms",
  components: {},
  props: {
    currentPlayBackTime: {
      type: Number,
    },
    waveformData: {
      type: Array,
      required : true
    },
    duration : {
      type : Number,
      required : true
    }
  },
  mounted(){

    this.drawWaveform(this.waveformData, ".stream-waveforms-bars");

  },
  methods: {
    drawWaveform(data, div) {
      // const MAX_POINTS = 1024;
      // let data = waveformData.slice(1, MAX_POINTS);
      let waveform = document.getElementsByClassName("stream-waveforms");
      let { width } = waveform[0].getBoundingClientRect();
      let height = 50;
      var y = d3.scaleLinear().range([height, -height]);
      var x = d3.scaleLinear().domain([0, data.length]);
      var max_val = d3.max(data, function (d) {
        return d;
      });
      y.domain([-max_val, max_val]);
      var bar_width = width / data.length;
      d3.select(div)
        .selectAll("div")
        .data(data)
        .enter()
        .append("div")
        .attr("class", "bar")
        .style("width", bar_width + "px")
        .style("height", function (d) {
          return y(d) + "px";
        })
        .style("bottom", function (d) {
          var bottom = height - Math.abs(y(d) / 2) - height / 2 + 2;
          return bottom + "px";
        })
        .style("left", function (d, i) {
          var left = x(i) * width;
          return left + "px";
        });
    },
    waveFormClicked(e) {
      var left = parseInt(e.target.style.left, 10);
      var rect = e.target.getBoundingClientRect();
      var x = 0;
      if (left) {
        x = left;
      } else {
        x = Math.abs(e.clientX - rect.left);
      }
      let waveform = document.getElementsByClassName("stream-waveforms");
      let { width } = waveform[0].getBoundingClientRect();
      let newTime = (x / width) * this.duration;
      this.$emit("waveform-clicked", newTime);
    },
  },
  watch: {
    currentPlayBackTime: {
      handler(newval) {
        if (this.$refs.cursor) {
          this.$refs.cursor.style.marginLeft =
            (newval / this.duration) * 100 + "%";
          let bars = document.getElementsByClassName("bar");
          if (bars.length) {
            [].forEach.call(bars, function (el) {
              el.classList.remove("active");
            });
            let activeIndex = (newval / this.duration) * bars.length;
            for (let index = 0; index <= activeIndex; index++) {
              const element = bars[index];
              element.classList.add("active");
            }
          }
        }
      },
    },
  },
};
</script>

<style lang="scss">
.stream-waveforms {
  width: 100%;
  height: 150px;
  position: relative;
  &-cursor {
    position: absolute;
    z-index: 1;
    height: 100%;
    width: 1px;
    background-color: #03a9f4;
    left: 0;
    transition: margin-left ease-in;
  }
}
.stream-waveforms-bars {
  //   border:       2px solid #ddd;
  height: 85px;
  top: 38px;
  //   margin-left:  40px;
  //   padding:      2px;
  position: relative;
  overflow-y: hidden;
  overflow-x: hidden;
  //   width:        880px;
}
.stream-waveforms-bars div.bar {
  background-color: #d0eefc;
  position: absolute;
}
.bar.active {
  background-color: #03a9f4!important;
  position: absolute;
}

.axis {
  position: absolute;
  top: 4px;
  left: -40px;
}
.axis g path.domain {
  display: none;
}

</style>