package com.example.demo;

// ───────────────────────────────────────────────
// IMPORTS: Librerías de Spring Boot
// ───────────────────────────────────────────────

import org.springframework.boot.builder.SpringApplicationBuilder;
// Clase que construye/configura una aplicación Spring Boot
// para que pueda ejecutarse como un servlet en un servidor externo.

import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;
// Clase base que permite inicializar Spring Boot como un servlet tradicional.
// Se usa cuando despliegas tu app en un servidor web externo (Tomcat, Jetty, etc.)
// en lugar de usar el Tomcat embebido.

// ───────────────────────────────────────────────
// ¿QUÉ ES ESTA CLASE Y PARA QUÉ SIRVE?
// ───────────────────────────────────────────────

// Tu proyecto tiene <packaging>war</packaging> en el pom.xml (no JAR).
// Esto significa que genera un archivo .war (Web Application Archive)
// que se puede desplegar en un servidor de aplicaciones externo.

// Cuando usas Tomcat EMBEBIDO (modo normal):
//   → No necesitas esta clase
//   → Spring Boot inicia Tomcat automáticamente
//   → Ejecutas: .\mvnw.cmd spring-boot:run

// Cuando usas un servidor EXTERNO (modo WAR):
//   → SÍ necesitas esta clase
//   → El servidor externo (Tomcat/JBoss/WebLogic) necesita saber cómo iniciar Spring Boot
//   → Esta clase hace de "puente" entre el servidor externo y tu app Spring Boot

// ───────────────────────────────────────────────
// DECLARACIÓN DE LA CLASE
// ───────────────────────────────────────────────

public class ServletInitializer extends SpringBootServletInitializer {
//     ↑              ↑
//     |              └── Hereda de SpringBootServletInitializer
//     |                  Proporciona el método configure() para inicializar la app
//     |
//     └── Nombre de la clase. Puede ser cualquier nombre, pero ServletInitializer
//         es el nombre convencional y recomendado por Spring Boot.

    // ═══════════════════════════════════════════════
    // MÉTODO: CONFIGURAR LA APLICACIÓN
    // ═══════════════════════════════════════════════
    // Este método es llamado automáticamente por el servidor web externo
    // cuando despliega el archivo .war

    @Override
    // Sobrescribe el método de la clase padre.
    // Indica que estamos reemplazando el comportamiento por defecto.

    protected SpringApplicationBuilder configure(SpringApplicationBuilder application) {
    //     ↑              ↑                           ↑
    //     |              |                           └── Recibe un builder (constructor) 
    //     |              |                               que configura la aplicación
    //     |              |
    //     |              └── Devuelve un SpringApplicationBuilder configurado
    //     |
    //     └── protected: solo accesible desde esta clase y subclases

        // ───────────────────────────────────────────────
        // INDICAR LA CLASE PRINCIPAL DE LA APLICACIÓN
        // ───────────────────────────────────────────────

        return application.sources(DemoApplication.class);
        //     ↑              ↑                    ↑
        //     |              |                    └── Tu clase principal (la que tiene @SpringBootApplication)
        //     |              |
        //     |              └── Método que indica cuál es la fuente principal de la app
        //     |
        //     └── Devuelve el builder configurado al servidor web externo

        // En resumen: le dice al servidor externo:
        // "Para iniciar esta aplicación Spring Boot, usa DemoApplication como punto de entrada"
    }
}