package com.yogapose.backend.controllers;

import com.yogapose.backend.models.Evaluation;
import com.yogapose.backend.models.User;
import com.yogapose.backend.repositories.EvaluationRepository;
import com.yogapose.backend.repositories.UserRepository;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/evaluations")
public class EvaluationController {
    private final EvaluationRepository evaluationRepository;
    private final UserRepository userRepository;

    public EvaluationController(EvaluationRepository evaluationRepository, UserRepository userRepository) {
        this.evaluationRepository = evaluationRepository;
        this.userRepository = userRepository;
    }

    @GetMapping("/{userId}")
    public List<Evaluation> getUserEvaluations(@PathVariable Long userId) {
        User user = userRepository.findById(userId).orElseThrow();
        return evaluationRepository.findByUser(user);
    }

    @PostMapping
    public Evaluation addEvaluation(@RequestBody Evaluation evaluation) {
        return evaluationRepository.save(evaluation);
    }
}
