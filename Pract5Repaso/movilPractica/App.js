import React, { useState } from "react";
import axios from "axios";

function App() {

  const [nombreLibro, setNombreLibro] = useState("");
  const [idLibro, setIdLibro] = useState("");
  const [idEliminar, setIdEliminar] = useState("");

  const API_URL = "http://localhost:5000/v1/libros/";

  //  Registrar libro
  const RegistrarLibro = async () => {
    const nuevoRegistro = {
      id: Date.now(),
      nombre: nombreLibro,
      identificador: idLibro
    };

    try {
      await axios.post(API_URL, nuevoRegistro);
      alert("Libro registrado correctamente");
      setNombreLibro("");
      setIdLibro("");
    } catch (error) {
      alert("Error al registrar libro");
    }
  };

  //  Eliminar registro de prestamo
  const eliminarRegistro = async () => {
    try {
      await axios.delete(`${API_URL}${idEliminar}`);
      alert("Registro eliminado correctamente");
      setIdEliminar("");
    } catch (error) {
      alert("Libro no encontrado");
    }
  };

  return (
    <div style={{ padding: "40px" }}>
      <h2>Registrar Libro</h2>

      <input
        type="text"
        placeholder="Nombre"
        value={nombreLibro}
        onChange={(e) => setNombreLibro(e.target.value)}
      />
      <br /><br />

      <input
        type="text"
        placeholder="Identificador"
        value={idLibro}
        onChange={(e) => setIdLibro(e.target.value)}
      />
      <br /><br />

      <button onClick={RegistrarLibro}>
        Registrar Libro
      </button>

      <hr />

      <h2>Eliminar Registro</h2>

      <input
        type="number"
        placeholder="ID del registro"
        value={idEliminar}
        onChange={(e) => setIdEliminar(e.target.value)}
      />
      <br /><br />

      <button onClick={eliminarRegistro}>
        Eliminar
      </button>

    </div>
  );
}

export default App;
