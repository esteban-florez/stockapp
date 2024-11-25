document.addEventListener('alpine:init', () => {
  Alpine.data('form', () => ({
    products: new Map(),
    selected: '',
    type: '',
    get product() {
      if (!this.selected || this.type !== 'minus') return
      return this.products.get(Number(this.selected))
    },
    get maxText() {
      if (!this.max) return
      return `(max. ${this.max})`
    },
    get max() {
      return this.product?.stock
    },
    init() {
      const products = JSON.parse(document.querySelector('#products-data').textContent)
      const old = JSON.parse(document.querySelector('#old-data').textContent)

      if (old) {
        this.selected = old.product
        this.type = old.type
      }

      products.forEach(product => {
        this.products.set(product.id, product)
      })
    },
  }))
})
