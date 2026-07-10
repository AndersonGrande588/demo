package com.example.medicamentos;

@RestController

public class MedicamentosControll {


        @GetMapping("/")
        public String prueba(){
        return "hola mundo";
    }
}
