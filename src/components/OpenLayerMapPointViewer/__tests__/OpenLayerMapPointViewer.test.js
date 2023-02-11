import { OpenLayerMapPointViewer } from ".."
import { mount } from "@vue/test-utils"

const createComponent = (options) => mount(OpenLayerMapPointViewer, options)

describe("OpenLayerMapPointViewer", () => {
  test("Render correctly", () => {
    const wrapper = createComponent()

    expect(wrapper.html()).toMatchSnapshot()
  })
  test("Render correctly - with the passed props", () => {
    const wrapper = createComponent({
      props: {
        positionsList: ["35.7040744", "139.5577317"],
        center: ["35.7040744", "139.5577317"],
      },
    })

    expect(wrapper.html()).toMatchSnapshot()
  })
})
