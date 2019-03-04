<template>
    <div>
        <div class="value" v-bind:style="{ width: width}">{{ word[2] }}</div>
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
      word: function (word) {
        let width = this.scaleFactor * word[1]
        this.width = `${width}px`
      },
      scaleFactor: function (word) {
        let width = this.scaleFactor * word[1]
        this.width = `${width}px`
      }
    }
  }
</script>

<style scoped>
    .title {
        color: #888;
        font-size: 18px;
        font-weight: initial;
        letter-spacing: .25px;
        margin-top: 10px;
    }

    .items {
        margin-top: 8px;
    }

    .item {
        display: flex;
        margin-bottom: 6px;
    }

    .item .name {
        color: #6a6a6a;
        margin-right: 6px;
    }

    .item .value {
        color: #35495e;
        font-weight: bold;
    }
</style>
