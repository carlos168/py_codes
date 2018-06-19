
<template>
  <div class="home">
    <el-row dispaly="margin-top:10px">
      <el-col :span="4"><el-input v-model="input" placeholder="请输入矿机名"></el-input></el-col>
      <el-button type="primary" @click="addMiner()">新增</el-button>
    </el-row>
    <el-row>
      <el-table :data="miner_list" style="width: 100%" border>
        <el-table-column prop="id" label="编号" min-width="100">
          <template scope="scope">{{scope.row.pk}}</template>
        </el-table-column>
        <el-table-column prop="miner_name" label="矿机" min-width="100">
          <template scope="scope">{{scope.row.fields.miner_name}}</template>
        </el-table-column>
        <el-table-column prop="ctm" label="添加时间" min-width="100">
          <template scope="scope">{{scope.row.fields.ctm}}</template>
        </el-table-column>
      </el-table>
    </el-row>
  </div>
</template>


<script>
export default {
  name: 'home',
  data () {
    return {
      input: '',
      miner_list: [],
    }
  },
  mounted: function() {
    console.log("==========2=====")
    this.showMiners()
  },

  methods: {
    addMiner(){
      console.log('新增 addMiner()')
      this.$http.get('http://localhost:8000/api/add_miner?miner_name=' + this.input)
        .then((response) => {
            var res = JSON.parse(response.bodyText)
            if (res.error_num == 0) {
              this.showBooks()
            } else {
              this.$message.error('新增矿机失败，请重试')
              console.log(res['msg'])
            }
        })
    },

    showMiners(){
      console.log('showMiners is called...')
      this.$http.get('http://localhost:8000/api/show_miners')
        .then((response) => {
            var res = JSON.parse(response.bodyText)
            console.log('=============')
            console.log(res)
            if (res.error_num == 0) {
              this.miner_list = res['list']
            } else {
              this.$message.error('查询书籍失败')
              console.log(res['msg'])
            }
        })
    }
  }
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>

