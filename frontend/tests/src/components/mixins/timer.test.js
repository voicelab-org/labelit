import { shallowMount } from "@vue/test-utils";
import MockComponent from "./MockComponent.vue";
import Timer from "@/components/mixins/Timer.js";

jest.useFakeTimers();

describe("Test Timer mixin", () => {
  it("starts the timer when startTimer() is called from wrapper component", () => {
    const wrapper = shallowMount(MockComponent, {
      mixins: [Timer],
    });
    expect(wrapper.vm.time).toBe(0);

    wrapper.find("div").trigger("click"); // triggers startTimer
    jest.advanceTimersByTime(3000);
    expect(wrapper.vm.time).toBeGreaterThan(0);
  });

  it("stops the timer and resets time to 0 after inactivity threshold", () => {
    const wrapper = shallowMount(MockComponent, {
      mixins: [Timer],
    });
    jest.useFakeTimers();
    expect(wrapper.vm.time).toBe(0);

    wrapper.find("div").trigger("click"); // triggers startTimer
    window.dispatchEvent(new Event("click")); // triggers activity listeners
    var thresh = wrapper.vm.batch.project.timer_inactivity_threshold;
    jest.advanceTimersByTime(thresh + 10);
    expect(wrapper.vm.time).toBeGreaterThan(0);

    const t = wrapper.vm.time;
    jest.advanceTimersByTime(3000);
    expect(wrapper.vm.time).toBe(0);
  });
});
