console.log(location.search) // lee los argumentos pasados a este formulario
var id=location.search.substr(4)
console.log(id)
const { createApp } = Vue
    createApp({
        data() {
            return {
                id:0,
                nombre:"",
                id_especie:"",                
                peso:0,
                imagen:"",
                url:'https://sebasrgomez90.pythonanywhere.com/mascotas/'+id,
            }
        },
        methods: {
            fetchData(url) {
                fetch(url)
                    .then(response => response.json())
                    .then(data => {
                    console.log(data)
                    this.id=data.id
                    this.nombre = data.nombre;
                    this.id_especie=data.id_especie;
                    this.peso=data.peso;
                    this.imagen=data.imagen;
                    
                    
            })
            .catch(err => {
                console.error(err);
                this.error=true
            })
    },
    modificar() {
        let mascota = {
            nombre:this.nombre,
            id_especie: this.id_especie,
            peso: this.peso,
            imagen:this.imagen
        }
        var options = {
            body: JSON.stringify(mascota),
            method:'PUT',
            headers: { 'Content-Type': 'application/json' },
            redirect: 'follow'
        }
        fetch(this.url, options)
            .then(function () {
                alert("Registro modificado")
                window.location.href = "./mascotas.html";
            })
            .catch(err => {
                console.error(err);
                alert("Error al Modificar")
            })
    }
    },
    created() {
    this.fetchData(this.url)
    },
    }).mount('#app')
