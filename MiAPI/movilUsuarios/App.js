import React, { useState } from "react";
import axios from "axios";

function App() {

  const [nombre, setNombre] = useState("");
  const [edad, setEdad] = useState("");
  const [idEliminar, setIdEliminar] = useState("");

  const API_URL = "http://127.0.0.1:8000/v1/usuarios/";

  // 🔹 Crear usuario
  const crearUsuario = async () => {
    const nuevoUsuario = {
      id: Date.now(),
      nombre: nombre,
      edad: edad
    };

    try {
      await axios.post(API_URL, nuevoUsuario);
      alert("Usuario creado correctamente");
      setNombre("");
      setEdad("");
    } catch (error) {
      alert("Error al crear usuario");
    }
  };

  // 🔹 Eliminar usuario
  const eliminarUsuario = async () => {
    try {
      await axios.delete(`${API_URL}${idEliminar}`);
      alert("Usuario eliminado correctamente");
      setIdEliminar("");
    } catch (error) {
      alert("Usuario no encontrado");
    }
  };

  return (
    <div style={{ padding: "40px" }}>
      <h2>Crear Usuario</h2>

      <input
        type="text"
        placeholder="Nombre"
        value={nombre}
        onChange={(e) => setNombre(e.target.value)}
      />
      <br /><br />

      <input
        type="text"
        placeholder="Edad"
        value={edad}
        onChange={(e) => setEdad(e.target.value)}
      />
      <br /><br />

      <button onClick={crearUsuario}>
        Crear
      </button>

      <hr />

      <h2>Eliminar Usuario</h2>

      <input
        type="number"
        placeholder="ID del usuario"
        value={idEliminar}
        onChange={(e) => setIdEliminar(e.target.value)}
      />
      <br /><br />

      <button onClick={eliminarUsuario}>
        Eliminar
      </button>

    </div>
  );
}

export default App;
