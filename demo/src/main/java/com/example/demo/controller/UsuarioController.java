package com.example.demo.controller;

// ───────────────────────────────────────────────
// IMPORTS: Librerías de Java y Spring Boot
// ───────────────────────────────────────────────

import java.util.ArrayList;   // Lista dinámica (array que crece automáticamente)
import java.util.Optional;    // Envuelve un objeto que puede o no existir (evita null)

import com.example.demo.models.UsuarioModel;   // Tu modelo/entidad de usuario
import com.example.demo.services.UsuarioService; // Tu clase de lógica de negocio

import org.springframework.beans.factory.annotation.Autowired; // Inyección automática de dependencias
import org.springframework.web.bind.annotation.*; // Todas las anotaciones para APIs REST

// ───────────────────────────────────────────────
// ANOTACIONES DE LA CLASE
// ───────────────────────────────────────────────

@RestController              // Dice que esta clase es un controlador REST (devuelve JSON, no HTML)
@RequestMapping("/usuario")  // Ruta base: TODAS las URLs de este controlador empiezan con /usuario
public class UsuarioController {

    // ───────────────────────────────────────────────
    // INYECCIÓN DE DEPENDENCIAS
    // ───────────────────────────────────────────────
    
    @Autowired                 // Spring crea automáticamente la instancia, no necesitas "new"
    UsuarioService usuarioService;  // Conexión con la capa de servicio (lógica de negocio)

    // ═══════════════════════════════════════════════
    // ENDPOINT 1: OBTENER TODOS LOS USUARIOS
    // ═══════════════════════════════════════════════
    // Método:   GET
    // URL:      http://localhost:8080/usuario
    // Acción:   Lista todos los usuarios de la base de datos
    
    @GetMapping()  // Responde a peticiones GET en /usuario
    public ArrayList<UsuarioModel> obtenerUsuarios(){  // CORREGIDO: "obetener" → "obtener"
        return usuarioService.obtenerUsuarios();
    }

    // ═══════════════════════════════════════════════
    // ENDPOINT 2: CREAR UN USUARIO
    // ═══════════════════════════════════════════════
    // Método:   POST
    // URL:      http://localhost:8080/usuario
    // Body:     JSON con los datos del usuario
    // Acción:   Guarda un nuevo usuario en la base de datos
    
    @PostMapping  // Responde a peticiones POST en /usuario
    public UsuarioModel guardarUsuario(@RequestBody UsuarioModel usuario){
        // @RequestBody → Convierte el JSON del body de la petición en un objeto UsuarioModel
        return this.usuarioService.guardarUsuario(usuario);  // CORREGIDO: "guardaru" → "guardar"
    }

    // ═══════════════════════════════════════════════
    // ENDPOINT 3: OBTENER UN USUARIO POR ID
    // ═══════════════════════════════════════════════
    // Método:   GET
    // URL:      http://localhost:8080/usuario/5
    // Acción:   Busca un usuario específico por su ID
    
    @GetMapping(path = "/{id}")  // {id} es una variable: puede ser cualquier número
    public Optional<UsuarioModel> obtenerUsuarioPorId(@PathVariable("id") Long id){
        // @PathVariable("id") → Extrae el valor de {id} de la URL y lo asigna al parámetro
        // Optional<> → Puede devolver el usuario o "vacío" si no existe (evita null pointer)
        return this.usuarioService.obtenerPorId(id);
    }

    // ═══════════════════════════════════════════════
    // ENDPOINT 4: BUSCAR USUARIOS POR PRIORIDAD
    // ═══════════════════════════════════════════════
    // Método:   GET
    // URL:      http://localhost:8080/usuario/query?prioridad=1
    // Acción:   Busca usuarios que tengan una prioridad específica
    
    @GetMapping("/query")  // Ruta específica: /usuario/query
    public ArrayList<UsuarioModel> obtenerUsuarioPorPrioridad(  // CORREGIDO: "Usuariio" → "Usuario"
            @RequestParam("prioridad") Integer prioridad ){
        // @RequestParam("prioridad") → Lee el parámetro de la URL (?prioridad=1)
        return this.usuarioService.obtenerPorPrioridad(prioridad);  // CORREGIDO: "Priorodad" → "Prioridad"
    }

    // ═══════════════════════════════════════════════
    // ENDPOINT 5: ELIMINAR UN USUARIO POR ID
    // ═══════════════════════════════════════════════
    // Método:   DELETE
    // URL:      http://localhost:8080/usuario/5
    // Acción:   Elimina un usuario de la base de datos
    
    @DeleteMapping(path = "/{id}")  // Responde a peticiones DELETE
    public String eliminarPorId(@PathVariable("id") Long id){
        boolean ok = this.usuarioService.eliminarUsuario(id);
        // El servicio devuelve true si se eliminó, false si no
        
        if(ok){
            return "Se eliminó el usuario con Id " + id;  // CORREGIDO: "eliminnno" → "eliminó"
        } else {
            return "No se pudo eliminar el usuario con Id " + id;  // CORREGIDO: mensaje más claro
        }
    }
}