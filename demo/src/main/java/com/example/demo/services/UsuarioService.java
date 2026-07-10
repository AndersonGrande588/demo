package com.example.demo.services;

// ───────────────────────────────────────────────
// IMPORTS: Librerías de Java y Spring Boot
// ───────────────────────────────────────────────

import java.util.ArrayList;
// Lista dinámica para devolver múltiples usuarios

import java.util.Optional;
// Envuelve un resultado que puede o no existir (evita null pointer)

import org.springframework.beans.factory.annotation.Autowired;
// Inyección automática de dependencias (Spring te da la instancia)

import org.springframework.stereotype.Service;
// Anotación que marca esta clase como servicio de negocio

import com.example.demo.models.UsuarioModel;
// Tu modelo/entidad de usuario

import com.example.demo.repositories.UsuarioRepository;
// Tu repositorio (acceso a base de datos)

// ───────────────────────────────────────────────
// ANOTACIÓN DE LA CLASE
// ───────────────────────────────────────────────

@Service
// Marca esta clase como un SERVICIO de Spring.
// Es la capa de LÓGICA DE NEGOCIO de tu aplicación.
// Se encuentra entre el Controller (API) y el Repository (BD).
// Spring detecta automáticamente esta clase y la registra como un "bean".
// Equivalente a @Component pero semánticamente indica "servicio de negocio".

// ───────────────────────────────────────────────
// DECLARACIÓN DE LA CLASE
// ───────────────────────────────────────────────

public class UsuarioService {
// Clase pública que contiene la lógica de negocio relacionada con usuarios.
// Aquí se procesan datos, se aplican reglas, se validan antes de guardar, etc.

    // ═══════════════════════════════════════════════
    // INYECCIÓN DE DEPENDENCIAS
    // ═══════════════════════════════════════════════

    @Autowired
    // Spring busca automáticamente una instancia de UsuarioRepository
    // y la asigna a esta variable. No necesitas hacer "new UsuarioRepository()".
    // Esto se llama "Inyección de Dependencias" (Dependency Injection).

    UsuarioRepository usuarioRepository;
    // Variable que te permite acceder a la base de datos a través del repositorio.
    // Es la conexión entre la lógica de negocio (Service) y los datos (Repository).

    // ═══════════════════════════════════════════════
    // MÉTODO 1: OBTENER TODOS LOS USUARIOS
    // ═══════════════════════════════════════════════
    // Acción:   Recupera TODOS los registros de la tabla usuario
    // Llama a:  usuarioRepository.findAll() (método heredado de CrudRepository)
    // Retorna:  ArrayList<UsuarioModel> con todos los usuarios

    public ArrayList<UsuarioModel> obtenerUsuarios(){
        // findAll() viene de CrudRepository y devuelve un Iterable<T>.
        // Se hace un "cast" (conversión) a ArrayList para que coincida con el tipo de retorno.
        return (ArrayList<UsuarioModel>) usuarioRepository.findAll();
    }

    // ═══════════════════════════════════════════════
    // MÉTODO 2: GUARDAR UN USUARIO
    // ═══════════════════════════════════════════════
    // Acción:   Crea un nuevo usuario o actualiza uno existente
    // Llama a:  usuarioRepository.save(usuario) (método heredado de CrudRepository)
    // Retorna:  El usuario guardado (con el ID asignado si es nuevo)
    // CORREGIDO: "guardaruUsuario" → "guardarUsuario"

    public UsuarioModel guardarUsuario(UsuarioModel usuario){
        // save() guarda el objeto en la base de datos.
        // Si el ID es null, INSERTA un nuevo registro.
        // Si el ID ya existe, ACTUALIZA el registro existente.
        return usuarioRepository.save(usuario);
    }

    // ═══════════════════════════════════════════════
    // MÉTODO 3: OBTENER UN USUARIO POR ID
    // ═══════════════════════════════════════════════
    // Acción:   Busca un usuario específico por su ID
    // Llama a:  usuarioRepository.findById(id) (método heredado de CrudRepository)
    // Retorna:  Optional<UsuarioModel> → el usuario o "vacío" si no existe

    public Optional<UsuarioModel> obtenerPorId(Long id){
        // Optional evita que devuelvas null.
        // Si el usuario existe: Optional contiene el objeto.
        // Si no existe: Optional está vacío (Optional.empty()).
        // El Controller puede verificar con .isPresent() o .orElse(null).
        return usuarioRepository.findById(id);
    }

    // ═══════════════════════════════════════════════
    // MÉTODO 4: OBTENER USUARIOS POR PRIORIDAD
    // ═══════════════════════════════════════════════
    // Acción:   Busca todos los usuarios que tengan una prioridad específica
    // Llama a:  usuarioRepository.findByPrioridad(prioridad) (TU MÉTODO PERSONALIZADO)
    // Retorna:  ArrayList<UsuarioModel> con los usuarios que coinciden
    // CORREGIDO: "obtenerPorPriorodad" → "obtenerPorPrioridad"

    public ArrayList<UsuarioModel> obtenerPorPrioridad(Integer prioridad){
        // findByPrioridad() es el método que TÚ definiste en UsuarioRepository.
        // Spring Data JPA generó automáticamente la consulta SQL:
        //   SELECT * FROM usuario WHERE prioridad = ?
        return usuarioRepository.findByPrioridad(prioridad);
    }

    // ═══════════════════════════════════════════════
    // MÉTODO 5: ELIMINAR UN USUARIO POR ID
    // ═══════════════════════════════════════════════
    // Acción:   Elimina un usuario de la base de datos por su ID
    // Llama a:  usuarioRepository.deleteById(id) (método heredado de CrudRepository)
    // Retorna:  true si se eliminó correctamente, false si hubo error

    public boolean eliminarUsuario(Long id){
        try {
            // Intenta eliminar el usuario.
            // deleteById() lanza una excepción si el ID no existe.
            usuarioRepository.deleteById(id);
            return true;  // Éxito: se eliminó sin problemas
        } catch(Exception err) {
            // Si ocurre cualquier error (ej: ID no existe, error de conexión):
            // Captura la excepción y devuelve false en lugar de romper la aplicación.
            return false;  // Fallo: no se pudo eliminar
        }
    }
}