package com.example.demo.repositories;

// ───────────────────────────────────────────────
// IMPORTS: Librerías de Java y Spring Boot
// ───────────────────────────────────────────────

import com.example.demo.models.UsuarioModel;
// Importa tu modelo de usuario (la entidad que representa la tabla en la BD)

import org.springframework.stereotype.Repository;
// Anotación que marca esta interfaz como un repositorio de datos

import java.util.ArrayList;
// Lista dinámica para devolver múltiples resultados

import org.springframework.data.repository.CrudRepository;
// Interfaz base de Spring Data que proporciona operaciones CRUD automáticas

// ───────────────────────────────────────────────
// ANOTACIÓN DE LA INTERFAZ
// ───────────────────────────────────────────────

@Repository
// Marca esta interfaz como un REPOSITORIO de Spring.
// Esto permite que Spring la detecte automáticamente y la registre como un bean.
// También indica que esta clase maneja operaciones de acceso a datos (base de datos).
// Equivalente a @Component pero específico para la capa de persistencia.

// ───────────────────────────────────────────────
// DECLARACIÓN DE LA INTERFAZ
// ───────────────────────────────────────────────

public interface UsuarioRepository extends CrudRepository<UsuarioModel, Long> {
//     ↑        ↑                    ↑
//     |        |                    └── Hereda de CrudRepository
//     |        |                        (proporciona métodos CRUD listos para usar)
//     |        |
//     |        └── Nombre de la interfaz
//     |
//     └── "interface" = NO tiene implementación, solo define qué métodos existen.
//         Spring Data JPA genera la implementación AUTOMÁTICAMENTE en tiempo de ejecución.

// ───────────────────────────────────────────────
// EXPLICACIÓN DE: extends CrudRepository<UsuarioModel, Long>
// ───────────────────────────────────────────────

// CrudRepository es una interfaz de Spring Data JPA que ya viene con métodos listos:
//
//   CREATE  → save(UsuarioModel usuario)        → Guarda/actualiza un usuario
//   READ    → findById(Long id)                → Busca por ID
//   READ    → findAll()                         → Busca TODOS los usuarios
//   UPDATE  → save(UsuarioModel usuario)        → (el mismo save actualiza si ya existe)
//   DELETE  → deleteById(Long id)               → Elimina por ID
//   DELETE  → delete(UsuarioModel usuario)        → Elimina el objeto
//   COUNT   → count()                           → Cuenta registros
//   EXISTS  → existsById(Long id)               → Verifica si existe
//
// <UsuarioModel, Long> significa:
//   - UsuarioModel = La entidad que maneja (tabla de la BD)
//   - Long         = El tipo de dato de la clave primaria (ID)

    // ═══════════════════════════════════════════════
    // MÉTODO PERSONALIZADO: Buscar por prioridad
    // ═══════════════════════════════════════════════
    
    public abstract ArrayList<UsuarioModel> findByPrioridad(Integer prioridad);
    //     ↑        ↑                    ↑
    //     |        |                    └── Nombre del método sigue convención de Spring Data
    //     |        |                        "findBy" + "Prioridad" = busca donde prioridad = ?
    //     |        |
    //     |        └── Spring Data JPA genera automáticamente la consulta SQL
    //     |            NO necesitas escribir la consulta manualmente
    //     |
    //     └── "abstract" es opcional en interfaces (todos los métodos de interfaz son abstractos)
    //         Puedes quitarlo y funciona igual

    // ───────────────────────────────────────────────
    // ¿CÓMO FUNCIONA findByPrioridad?
    // ───────────────────────────────────────────────
    
    // Spring Data JPA analiza el nombre del método y genera automáticamente:
    //   SELECT * FROM usuario WHERE prioridad = ?
    //
    // La convención es: findBy + [NombreDelCampo]
    //   findByPrioridad    → WHERE prioridad = ?
    //   findByNombre       → WHERE nombre = ?
    //   findByEmail        → WHERE email = ?
    //
    // También puedes combinar:
    //   findByNombreAndEmail      → WHERE nombre = ? AND email = ?
    //   findByNombreOrPrioridad   → WHERE nombre = ? OR prioridad = ?
    //   findByNombreContaining    → WHERE nombre LIKE '%?%'
    //   findByPrioridadGreaterThan → WHERE prioridad > ?

}