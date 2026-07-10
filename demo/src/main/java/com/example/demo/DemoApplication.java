package com.example.demo;

// ───────────────────────────────────────────────
// IMPORTS: Librerías de Spring Boot
// ───────────────────────────────────────────────

import org.springframework.boot.SpringApplication;
// Clase principal que lanza (inicia) la aplicación Spring Boot.
// Contiene el método estático run() que arranca todo.

import org.springframework.boot.autoconfigure.SpringBootApplication;
// Anotación "mágica" que configura automáticamente toda la aplicación.
// Es la combinación de 3 anotaciones en una sola (ver más abajo).

// ───────────────────────────────────────────────
// ANOTACIÓN PRINCIPAL
// ───────────────────────────────────────────────

@SpringBootApplication
// Esta anotación es EQUIVALENTE a poner estas 3 anotaciones juntas:
//
//   @Configuration        → Marca la clase como fuente de configuración de beans
//   @EnableAutoConfiguration → Spring Boot configura automáticamente todo 
//                              (base de datos, servidor web, seguridad, etc.)
//   @ComponentScan        → Escanea automáticamente todas las clases anotadas
//                            (@Controller, @Service, @Repository, @Component)
//                            en el mismo paquete y subpaquetes
//
// En resumen: CON ESTA ANOTACIÓN SOLA, Spring Boot:
//   1. Escanea tu proyecto buscando componentes
//   2. Crea automáticamente las conexiones a base de datos
//   3. Configura el servidor web (Tomcat)
//   4. Inicia todo sin que tú escribas configuración XML

// ───────────────────────────────────────────────
// DECLARACIÓN DE LA CLASE
// ───────────────────────────────────────────────

public class DemoApplication {
// Esta es la clase PRINCIPAL de tu aplicación Spring Boot.
// Es el PUNTO DE ENTRADA: cuando ejecutas la app, Java corre este archivo primero.
// El nombre "DemoApplication" viene de cuando creaste el proyecto (puedes cambiarlo).

    // ═══════════════════════════════════════════════
    // MÉTODO MAIN: Punto de entrada de la aplicación
    // ═══════════════════════════════════════════════
    // Es el PRIMER método que se ejecuta cuando corres la aplicación.
    // Es estático (static) para que Java pueda llamarlo sin crear una instancia de la clase.

    public static void main(String[] args) {
    //     ↑       ↑      ↑
    //     |       |      └── Parámetros de línea de comandos (puedes pasar configuraciones)
    //     |       └── El método no devuelve nada (void)
    //     └── Público y estático: Java puede ejecutarlo directamente

        // ───────────────────────────────────────────────
        // LANZAR LA APLICACIÓN SPRING BOOT
        // ───────────────────────────────────────────────

        SpringApplication.run(DemoApplication.class, args);
        //     ↑              ↑                    ↑      ↑
        //     |              |                    |      |
        //     |              |                    |      └── Argumentos de línea de comandos
        //     |              |                    |
        //     |              |                    └── Clase principal (esta misma clase)
        //     |              |                        Spring usa esta clase como referencia
        //     |              |                        para saber dónde empezar a escanear
        //     |              |
        //     |              └── Método estático que ARRANCA TODO:
        //     |                  1. Crea el ApplicationContext (contenedor de Spring)
        //     |                  2. Registra todos los beans (@Controller, @Service, etc.)
        //     |                  3. Configura el servidor embebido (Tomcat en puerto 8080)
        //     |                  4. Inicia el servidor y deja la app corriendo
        //     |
        //     └── Clase de Spring Boot que contiene el método run()

    }
}