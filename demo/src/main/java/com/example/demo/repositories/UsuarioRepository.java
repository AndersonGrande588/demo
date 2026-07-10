package com.example.demo.repositories;

import com.example.demo.models.UsuarioModel;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;

import org.springframework.data.repository.CrudRepository;

@Repository
public interface UsuarioRepository extends CrudRepository<UsuarioModel, Long> {
    
    public abstract ArrayList<UsuarioModel> findByPrioridad(Integer prioridad);
}
