package com.yogapose.backend.repositories;

import com.yogapose.backend.models.Pose;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PoseRepository extends JpaRepository<Pose, Long> {
}
