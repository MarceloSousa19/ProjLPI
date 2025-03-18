package com.yogapose.backend.repositories;

import com.yogapose.backend.models.Evaluation;
import com.yogapose.backend.models.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface EvaluationRepository extends JpaRepository<Evaluation, Long> {
    List<Evaluation> findByUser(User user);
}
