package com.yogapose.backend.models;

import jakarta.persistence.*;
import lombok.Data;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import java.util.UUID;

@Entity
@Data
@Table(name = "usuarios")
public class User {
    @Id
    @GeneratedValue
    private UUID id;

    private String nome;
    private String email;
    private String senha;

    @Column(name = "data_registro")
    private java.time.LocalDateTime dataRegistro;

    public void setSenha(String senha) {
        this.senha = new BCryptPasswordEncoder().encode(senha);
    }
}
