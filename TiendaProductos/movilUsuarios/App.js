import React, { useEffect, useState } from "react";
import { View, Text, FlatList, TextInput, Button, TouchableOpacity, StyleSheet } from "react-native";
import axios from "axios";

const API = "http://10.16.39.51:5000"; 

export default function App() {

  const [productos, setProductos] = useState([]);
  const [editando, setEditando] = useState(false);

  const [id, setId] = useState("");
  const [nombre, setNombre] = useState("");
  const [precio, setPrecio] = useState("");
  const [stock, setStock] = useState("");
  const [categoria, setCategoria] = useState("");

  const obtenerProductos = async () => {
    try {
      const res = await axios.get(`${API}/v1/product/`);
      setProductos(res.data);
    } catch (error) {
      console.log(error);
    }
  };

  const agregarProducto = async () => {
    try {
      await axios.post(`${API}/v1/product/`, {
        id: parseInt(id),
        nombre,
        precio: parseFloat(precio),
        stock: parseInt(stock),
        categoria
      });
      obtenerProductos();
      limpiar();
    } catch (error) {
      console.log(error);
    }
  };

  const actualizarProducto = async () => {
    try {
      await axios.put(`${API}/v1/products/${id}`, {
        id: parseInt(id),
        nombre,
        precio: parseFloat(precio),
        stock: parseInt(stock),
        categoria
      });
      obtenerProductos();
      limpiar();
    } catch (error) {
      console.log(error);
    }
  };

  const eliminarProducto = async (id) => {
    try {
      await axios.delete(`${API}/v1/products/${id}`, {
        auth: {
          username: "ruth",
          password: "123456"
        }
      });
      obtenerProductos();
    } catch (error) {
      console.log(error);
    }
  };

  const cargarEdicion = (item) => {
    setId(item.id.toString());
    setNombre(item.nombre);
    setPrecio(item.precio.toString());
    setStock(item.stock.toString());
    setCategoria(item.categoria);
    setEditando(true);
  };

  const limpiar = () => {
    setId("");
    setNombre("");
    setPrecio("");
    setStock("");
    setCategoria("");
    setEditando(false);
  };

  useEffect(() => {
    obtenerProductos();
  }, []);

  return (
    <View style={styles.container}>

      <Text style={styles.title}>Tienda de productos</Text>

      <View style={styles.form}>

        {editando && <Text style={styles.modoEdicion}>Editando producto #{id}</Text>}

        <TextInput placeholder="ID" style={styles.input} onChangeText={setId} value={id} />
        <TextInput placeholder="Nombre" style={styles.input} onChangeText={setNombre} value={nombre} />
        <TextInput placeholder="Precio" style={styles.input} onChangeText={setPrecio} value={precio} />
        <TextInput placeholder="Stock" style={styles.input} onChangeText={setStock} value={stock} />
        <TextInput placeholder="Categoría" style={styles.input} onChangeText={setCategoria} value={categoria} />

        <Button
          title={editando ? "Guardar cambios" : "Agregar producto"}
          onPress={editando ? actualizarProducto : agregarProducto}
          color="#4a6cf7"
        />

        {editando && (
          <TouchableOpacity onPress={limpiar} style={styles.botonCancelar}>
            <Text style={styles.textoCancelar}>Cancelar edición</Text>
          </TouchableOpacity>
        )}

      </View>

      <FlatList
        data={productos}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.card}>

            <Text style={styles.name}>{item.nombre}</Text>
            <Text style={styles.detalle}>Precio: ${item.precio}</Text>
            <Text style={styles.detalle}>Stock: {item.stock}</Text>
            <Text style={styles.detalle}>Categoría: {item.categoria}</Text>

            <View style={styles.cardBotones}>
              <TouchableOpacity style={styles.botonEditar} onPress={() => cargarEdicion(item)}>
                <Text style={styles.textoEditar}>Editar</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.botonEliminar} onPress={() => eliminarProducto(item.id)}>
                <Text style={styles.textoEliminar}>Eliminar</Text>
              </TouchableOpacity>
            </View>

          </View>
        )}
      />

    </View>
  );
}

const styles = StyleSheet.create({

  container: {
    flex: 1,
    marginTop: 40,
    padding: 20,
    backgroundColor: "#f5f5f5"
  },

  title: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 16,
    color: "#222"
  },

  form: {
    backgroundColor: "#fff",
    padding: 14,
    borderRadius: 10,
    marginBottom: 20,
    borderWidth: 1,
    borderColor: "#e0e0e0"
  },

  modoEdicion: {
    color: "#4a6cf7",
    fontWeight: "600",
    marginBottom: 8,
    fontSize: 13
  },

  input: {
    borderWidth: 1,
    borderColor: "#ccc",
    padding: 10,
    marginBottom: 10,
    borderRadius: 6,
    backgroundColor: "#fafafa",
    color: "#333"
  },

  botonCancelar: {
    marginTop: 8,
    alignItems: "center"
  },

  textoCancelar: {
    color: "#999",
    fontSize: 13
  },

  card: {
    backgroundColor: "#fff",
    padding: 14,
    marginVertical: 6,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: "#e0e0e0"
  },

  name: {
    fontSize: 17,
    fontWeight: "bold",
    marginBottom: 4,
    color: "#222"
  },

  detalle: {
    fontSize: 14,
    color: "#555",
    marginBottom: 2
  },

  cardBotones: {
    flexDirection: "row",
    gap: 8,
    marginTop: 10
  },

  botonEditar: {
    flex: 1,
    backgroundColor: "#eef0ff",
    padding: 8,
    borderRadius: 6,
    alignItems: "center"
  },

  textoEditar: {
    color: "#4a6cf7",
    fontWeight: "600"
  },

  botonEliminar: {
    flex: 1,
    backgroundColor: "#fff0f0",
    padding: 8,
    borderRadius: 6,
    alignItems: "center"
  },

  textoEliminar: {
    color: "#e53935",
    fontWeight: "600"
  }

});