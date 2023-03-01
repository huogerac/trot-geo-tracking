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

  test("02 - deve salvar o primeiro ponto", () => {
    const store = useLocationStore()
    store.savePositions({ longitude: -49.015, latitude: -28.504, latLongAccuracy: 17.28 })
    expect(store.latLon).toEqual([[-49.015, -28.504]])
  })

  test("03 - deve salvar o primeiro ponto mesmo com uma acurácia RUIM", () => {
    const store = useLocationStore()
    store.savePositions({ longitude: -49.015, latitude: -28.504, latLongAccuracy: 102.28 })
    expect(store.latLon).toEqual([[-49.015, -28.504]])
  })

  test("04 - deve salvar pontos descartando os com acurácia ruim", () => {
    const store = useLocationStore()
    store.savePositions({ longitude: -49.015, latitude: -28.501, latLongAccuracy: 4 })
    store.savePositions({ longitude: -49.025, latitude: -28.511, latLongAccuracy: 3 })
    store.savePositions({ longitude: -49.035, latitude: -28.521, latLongAccuracy: 8 })
    // Ponto bem ruim recebido
    store.savePositions({ longitude: -49.235, latitude: -28.621, latLongAccuracy: 48 })
    store.savePositions({ longitude: -49.045, latitude: -28.531, latLongAccuracy: 12 })

    expect(store.latLon).toEqual([
      [-49.015, -28.501],
      [-49.025, -28.511],
      [-49.035, -28.521],
      [-49.045, -28.531],
    ])
  })

  test("5-deve descartar pontos ruins", () => {
    /**
     * Dado um percurso com as acurácias abaixo, escartar os pontos ruins
     *  1) 20.534
     *  2) 21.691
     *  3) 21.472
     *  4) 52.400  <-- DESCARTAR
     *  5) 35.805  <-- DESCARTAR
     *  6) 17.576
     *  7) 19.475
     *  9) 31.805  <-- DESCARTAR
     * 11) 21.267
     * 12) 21.444
     * 13) 18.283
     */

    const store = useLocationStore()

    store.savePositions({ longitude: 1.1, latitude: -1.1, latLongAccuracy: 20.534 })
    store.savePositions({ longitude: 1.2, latitude: -1.2, latLongAccuracy: 21.691 })
    store.savePositions({ longitude: 1.3, latitude: -1.3, latLongAccuracy: 21.472 })
    store.savePositions({ longitude: 1.4, latitude: -1.4, latLongAccuracy: 52.4 })
    store.savePositions({ longitude: 1.5, latitude: -1.5, latLongAccuracy: 35.805 })
    store.savePositions({ longitude: 1.6, latitude: -1.6, latLongAccuracy: 17.576 })
    store.savePositions({ longitude: 1.7, latitude: -1.7, latLongAccuracy: 19.475 })
    store.savePositions({ longitude: 1.8, latitude: -1.8, latLongAccuracy: 31.805 })
    store.savePositions({ longitude: 1.9, latitude: -1.9, latLongAccuracy: 21.267 })
    store.savePositions({ longitude: 1.11, latitude: -1.11, latLongAccuracy: 21.444 })
    store.savePositions({ longitude: 1.12, latitude: -1.12, latLongAccuracy: 18.283 })

    expect(store.latLon).toEqual([
      [1.1, -1.1],
      [1.2, -1.2],
      [1.3, -1.3],
      [1.6, -1.6],
      [1.7, -1.7],
      [1.9, -1.9],
      [1.11, -1.11],
      [1.12, -1.12],
    ])
  })

  test("6-deve descartar pontos ruins, mas saber qdo a acurácia geral é ruim", () => {
    /**
     * Dado um percurso onde a acurácia geral é ruim, saber não descartar tudo
     * e salvar os melhores pontos
     *  1) 33.820
     *  2) 30.820
     *  3) 58.669 <-- DESCARTAR
     *  4) 65.694 <-- DESCARTAR
     *  5) 21.621
     *  6) 34.820
     *  7) 42.842 <-- DESCARTAR
     *  8) 18.524
     *  9) 21.197
     * 11) 19.586
     * 12) 39.675 <-- DESCARTAR
     * 13) 42.138 <-- DESCARTAR
     * 14) 26.232
     * 15) 19.958
     * 16) 28.347
     * 17) 22.572
     */

    const store = useLocationStore()

    store.savePositions({ longitude: 1.1, latitude: -1.1, latLongAccuracy: 33.82 })
    store.savePositions({ longitude: 1.2, latitude: -1.2, latLongAccuracy: 30.82 })
    store.savePositions({ longitude: 1.3, latitude: -1.3, latLongAccuracy: 58.669 })
    store.savePositions({ longitude: 1.4, latitude: -1.4, latLongAccuracy: 65.694 })
    store.savePositions({ longitude: 1.5, latitude: -1.5, latLongAccuracy: 21.621 })
    store.savePositions({ longitude: 1.6, latitude: -1.6, latLongAccuracy: 34.82 })
    store.savePositions({ longitude: 1.7, latitude: -1.7, latLongAccuracy: 42.842 })
    store.savePositions({ longitude: 1.8, latitude: -1.8, latLongAccuracy: 18.524 })
    store.savePositions({ longitude: 1.9, latitude: -1.9, latLongAccuracy: 21.197 })
    store.savePositions({ longitude: 1.11, latitude: -1.11, latLongAccuracy: 19.586 })
    store.savePositions({ longitude: 1.12, latitude: -1.12, latLongAccuracy: 39.675 })
    store.savePositions({ longitude: 1.13, latitude: -1.13, latLongAccuracy: 42.138 })
    store.savePositions({ longitude: 1.14, latitude: -1.14, latLongAccuracy: 26.232 })
    store.savePositions({ longitude: 1.15, latitude: -1.15, latLongAccuracy: 19.958 })
    store.savePositions({ longitude: 1.16, latitude: -1.16, latLongAccuracy: 28.347 })
    store.savePositions({ longitude: 1.17, latitude: -1.17, latLongAccuracy: 22.572 })

    expect(store.latLon).toEqual([
      [1.1, -1.1],
      [1.2, -1.2],
      [1.5, -1.5],
      [1.6, -1.6],
      [1.8, -1.8],
      [1.9, -1.9],
      [1.11, -1.11],
      [1.14, -1.14],
      [1.15, -1.15],
      [1.16, -1.16],
      [1.17, -1.17],
    ])
  })

  test("07 - Descarta salvar posições iguais", () => {
    /**
     * O GPS do fone muitas vezes retorna o mesmo ponto (lat, lon exatamente iguais)
     * várias vezes, podemos salvar apenas uma vez
     */
    const store = useLocationStore()

    store.savePositions({ longitude: 1.111, latitude: -1.111, latLongAccuracy: 3.82 })
    store.savePositions({ longitude: 1.111, latitude: -1.111, latLongAccuracy: 3.82 })
    store.savePositions({ longitude: 1.111, latitude: -1.111, latLongAccuracy: 3.82 })

    expect(store.latLon).toEqual([[1.111, -1.111]])
  })
})
