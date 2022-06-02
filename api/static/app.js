  const { createApp } = Vue

  createApp({

    data() {
      return {
        fileName: null,
        file: null,
        image: null,
        score: null,
        prediction: null,
        scoreFormat: null,
        predictionFormat: null,
        loading: false,
        mje: false,
        errors: false,
        hashFile: false
      }
    },

    methods: {
        reset(){
          this.fileName = null
          this.file = null 
          this.image = null
          this.score = null
          this.prediction = null
          this.loading = false
          this.$refs.inputFile.value=null
          this.mje = false,
          this.errors = false,
          this.hashFile = false

        },

        handleFile(e) {
          const files = Array.from(e.target.files) || null
          this.setFile(files)
        },

        dropFile(e){
          const files = e.dataTransfer.files
          this.setFile(files)
        },


        setFile(files){
          if(files && files.length > 0){
            this.fileName = files[0].name
            this.file = files[0]
          }
        },

        async handleUpload(){
          let data = new FormData()
          data.append('file', this.file)
          data.append('front', 1)
          this.loading = true
          const response = await fetch('/predict', {
                                        method: 'POST',
                                        body: data
                                    })
            
          const jsonData = await response.json()
          this.processData(jsonData)                          
          this.loading = false

        },

        processData(jsonData){

          if(jsonData['success']){

            this.score = jsonData['score']
            this.scoreFormat = parseFloat(this.score * 100).toFixed(2)+"%"
            
            // remove underscore and uppercase first letter
            this.prediction = jsonData['prediction']
            this.predictionFormat  = this.prediction.charAt(0).toUpperCase() + this.prediction.slice(1);
            this.predictionFormat = this.predictionFormat .replace('_', ' ')
            this.hashFile = jsonData['file_name']
            this.image = '/static/uploads/' + this.hashFile
            this.errors = false
            return true

          } else {
            this.errors = jsonData['error']
            return false
          }
          
        },

        feedback(feedback){
          // if it was incorrect prediction call feedback endpoint
          if(!feedback){
            let data = new FormData()
            const report = `{'filename': '${this.hashFile}', 'prediction': '${this.prediction}', 'score':  ${this.score}}`

            data.append('report', report)
            data.append('front', 1)
            fetch('/feedback', {
              method: "POST",          
              body: data
            })

            this.mje = 'Sorry, It can fail'
          } else {
            this.mje = 'Perfect, thank you!'
          }
        }
    },
    delimiters: ['[[',']]']
  }).mount('#app')
