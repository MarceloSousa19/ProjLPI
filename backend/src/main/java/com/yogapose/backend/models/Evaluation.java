package com.yogapose.backend.models;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Data
@Table(name = "avaliacoes")
public class Evaluation {
    @Id
    @GeneratedValue
    private UUID id;

    @ManyToOne
    @JoinColumn(name = "usuario_id", nullable = false)
    private User user;

    @ManyToOne
    @JoinColumn(name = "pose_id", nullable = false)
    private Pose pose;

    private LocalDateTime data;
    private String resultado;
    private double similaridade;
}
