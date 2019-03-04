<template>
    <div>
        <div class="value" v-bind:style="{ width: getWidth}">{{ word[2] }}</div>
    </div>
</template>

<script>
  export default {
    props: ['word', 'scaleFactor'],
    data: function () {
      let width = this.scaleFactor * this.word[1]
      return {width: `${width}px`}
    },
    watch: {
      word: function () {
        let width = this.scaleFactor * this.word[1]
        this.width = `${width}px`
      },
      scaleFactor: function () {
        let width = this.scaleFactor * this.word[1]
        this.width = `${width}px`
        // console.log(this.word[1])
      }
    },
    computed: {
      getWidth: function () {
        return this.width
      }
    }
  }
</script>

<style scoped>

    .value {
        background-color: aquamarine;
        border: 2px solid #333333;
        margin: 2px;
        color: #35495e;
        font-weight: bold;
    }
</style>
