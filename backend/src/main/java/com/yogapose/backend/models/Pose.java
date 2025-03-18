package com.yogapose.backend.models;

import jakarta.persistence.*;
import lombok.Data;
import java.util.UUID;

@Entity
@Data
@Table(name = "poses")
public class Pose {
    @Id
    @GeneratedValue
    private UUID id;

    private String nome;
    private String descricao;
    private String categoria;
    private String imagem_url;

    @Column(columnDefinition = "jsonb")
    private String pontos_corporais;
}
