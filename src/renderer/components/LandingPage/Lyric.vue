<template>
    <div>
        <div class="title">
            <button @click="upscale()">+</button>
            <button @click="downscale">-</button>
            <button @click="print">print</button>
        </div>
        <div class="items">
            <div class="item">
                <div class="value" v-for="item in lyricData.data">
                    <word v-bind:scale-factor="scaleFactor" v-bind:word="item"></word>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
  import Word from './Lyric/Word'

  export default {
    components: {Word},
    props: ['lyricData'],
    data: function () {
      return {scaleFactor: 0.2}
    },
    methods: {
      upscale: function () {
        this.scaleFactor = this.scaleFactor * 1.5
        console.log(this.scaleFactor)
      },
      downscale: function () {
        this.scaleFactor /= 1.5
        console.log(this.scaleFactor)
      },
      print: function () {
        console.log(this.lyricData)
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
