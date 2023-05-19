new Vue({
    el: '#app',
    data: {
        message : 'Salut les gens',
        link : "file:///C:/Users/guilh/OneDrive/Documents/MES%20FICHIERS/INFO/S7/Ptrans/Training/index.html",
        success : true,
        persons: ["John","Gui"]
    },

    methods:{
        close : function(){
            
            this.success = false
        }
    }

})