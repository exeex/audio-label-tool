<template>
    <div class="field">
        <div class="value field-value" v-show="!showField('word')" v-bind:style="{ width: width}"
             @dblclick="focusField('word')" @blur="blurField">{{ word[2] }}
        </div>
        <input class="field-value form-control"
               ref="inputBox"
               type="text"
               v-bind:style="{ width: width}"
               v-show="showField('word')"
               v-model="word[2]"
               @focus="focusField('word')"
               @blur="blurField"/>
    </div>
</template>

<script>
  export default {
    props: ['word', 'scaleFactor'],
    data: function () {
      let width = this.scaleFactor * this.word[1] - 4
      return {width: `${width}px`, editField: ''}
    },
    methods: {
      focusField (name) {
        this.editField = name + this.word[2]
        this.$nextTick(() => this.$refs.inputBox.focus())
      },
      blurField () {
        this.editField = ''
      },
      showField (name) {
        return this.editField === name + this.word[2]
      }
    },
    watch: {
      word: function () {
        let width = this.scaleFactor * this.word[1] - 4
        this.width = `${width}px`
      },
      scaleFactor: function () {
        let width = this.scaleFactor * this.word[1] - 4
        this.width = `${width}px`
        // console.log(this.word[1])
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
