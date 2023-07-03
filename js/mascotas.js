const { createApp } = Vue

    createApp({
            data() {
                return {
                    mascotas: [],
                    url: 'https://sebasrgomez90.pythonanywhere.com/mascotas',
                    error: false,
                    cargando: true,
                    id: 0,
                    nombre: "",
                    id_especie: "",
                    peso: 0,
                    imagen: "",
                }
            },
            methods: {
                fetchData(url) {
                    fetch(url)
                        .then(response => response.json())
                        .then(data => {
                            this.mascotas = data;
                            this.cargando = false
                        })
                        .catch(err => {
                            console.error(err);
                            this.error = true
                        })
                },
                eliminar(mascota) {
                    const url = this.url + '/' + mascota;
                    var options = {
                        method: 'DELETE',
                    }
                    fetch(url, options)
                        .then(res => res.text()) // or res.json()
                        .then(res => {
                            location.reload();
                        })
                },
                grabar() {
                    let mascota = {
                    nombre: this.nombre,
                    id_especie: this.id_especie,
                    peso: this.peso,
                    imagen: this.imagen,
                }
                    var options = {
                        body: JSON.stringify(mascota),
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json', },
                        redirect: 'follow'
                    }
                    fetch(this.url, options)
                        .then(function () {
                            alert("Registro grabado");
                            window.location.href = "./mascotas.html";
                        })
                        .catch(err => {
                            console.error(err);
                            alert("Error al Grabar")
                        })
                    }
                    },
                    created() {
                    this.fetchData(this.url)
                    },
                    }).mount('#app')
