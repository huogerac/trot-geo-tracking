import { setActivePinia, createPinia } from "pinia"
import { beforeEach, expect, describe, test } from "vitest"
import { useLocationStore } from "@/store/location"

describe("Testa location store: Salvar Posições", () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  test("01 - Deve iniciar com a lista de posições vazia", () => {
    const store = useLocationStore()
    expect(store.latLon).toEqual([])
  })
})
