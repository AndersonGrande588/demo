package com.example.demo.models;

// ───────────────────────────────────────────────
// IMPORTS: Librerías de JPA (Jakarta Persistence API)
// ───────────────────────────────────────────────

import jakarta.persistence.*;
// El asterisco * importa TODAS las clases del paquete jakarta.persistence:
//   @Entity, @Table, @Id, @GeneratedValue, @Column, etc.

// ───────────────────────────────────────────────
// ANOTACIONES DE LA CLASE
// ───────────────────────────────────────────────

@Entity
// Marca esta clase como una ENTIDAD JPA.
// Esto significa que Hibernate (a través de Spring Data JPA) 
// mapeará esta clase a una tabla en la base de datos.

@Table(name="usuario")
// Define el nombre de la tabla en la base de datos.
// Si no pones esta anotación, Hibernate usaría el nombre de la clase como tabla.
// Aquí la tabla se llama "usuario" (en minúscula).

public class UsuarioModel {
// Clase pública que representa la entidad "Usuario" en la base de datos.
// "Model" indica que es el modelo de datos (capa de datos/entidad).

    // ═══════════════════════════════════════════════
    // ATRIBUTOS (COLUMNAS DE LA TABLA)
    // ═══════════════════════════════════════════════

    @Id
    // Marca este campo como la CLAVE PRIMARIA (Primary Key) de la tabla.
    // Cada registro debe tener un ID único para identificarlo.

    @GeneratedValue(strategy = GenerationType.IDENTITY)
    // Indica que el ID se genera AUTOMÁTICAMENTE.
    // GenerationType.IDENTITY = La base de datos genera el ID (auto-increment).
    // No necesitas asignar el ID manualmente, MySQL/PostgreSQL lo hace solo.

    @Column(unique = true, nullable = false)
    // Configura propiedades de la columna en la base de datos:
    //   unique = true  → No puede haber dos registros con el mismo ID
    //   nullable = false → No puede ser NULL (siempre debe tener valor)
    private Long id;
    // Tipo Long (número entero largo) para el ID.
    // Usamos Long (objeto) en lugar de long (primitivo) porque JPA lo recomienda.

    private String nombre;
    // Campo para el nombre del usuario.
    // @Column no es necesario aquí porque Hibernate usa el nombre del campo como columna.
    // Se mapea automáticamente a una columna VARCHAR en la base de datos.

    private String email;
    // Campo para el correo electrónico.
    // También se mapea automáticamente a VARCHAR.

    private Integer prioridad;
    // Campo numérico para la prioridad del usuario.
    // Integer (objeto) en lugar de int (primitivo) porque puede ser NULL en la BD.

    // ═══════════════════════════════════════════════
    // MÉTODOS GETTERS Y SETTERS
    // ═══════════════════════════════════════════════
    // Estos métodos permiten leer (get) y modificar (set) los atributos privados.
    // Son necesarios porque los atributos son "private" (no se pueden acceder directamente).

    // ─── PRIORIDAD ───
    public void setPrioridad(Integer prioridad){
        // SETTER: Asigna un valor a la prioridad.
        // "this.prioridad" = atributo de la clase
        // "prioridad" = parámetro que recibe el método
        this.prioridad = prioridad;
    }

    public Integer getPrioridad(){
        // GETTER: Devuelve (retorna) el valor actual de la prioridad.
        return prioridad;
    }

    // ─── ID ───
    public Long getId() {
        // GETTER: Devuelve el ID del usuario.
        // Normalmente no hay setter para ID porque se genera automáticamente.
        return id;
    }

    public void setId(Long id) {
        // SETTER: Permite modificar el ID (raramente se usa, pero útil para actualizaciones).
        this.id = id;
    }

    // ─── NOMBRE ───
    public String getNombre() {
        // GETTER: Devuelve el nombre del usuario.
        return nombre;
    }

    public void setNombre(String nombre) {
        // SETTER: Cambia el nombre del usuario.
        this.nombre = nombre;
    }

    // ─── EMAIL ───
    public String getEmail() {
        // GETTER: Devuelve el email del usuario.
        return email;
    }

    public void setEmail(String email) {
        // SETTER: Cambia el email del usuario.
        this.email = email;
    }

}