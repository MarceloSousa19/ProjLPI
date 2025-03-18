package com.yogapose.backend.controllers;

import com.yogapose.backend.models.Pose;
import com.yogapose.backend.repositories.PoseRepository;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/poses")
public class PoseController {
    private final PoseRepository poseRepository;

    public PoseController(PoseRepository poseRepository) {
        this.poseRepository = poseRepository;
    }

    @GetMapping
    public List<Pose> getAllPoses() {
        return poseRepository.findAll();
    }

    @PostMapping
    public Pose addPose(@RequestBody Pose pose) {
        return poseRepository.save(pose);
    }
}
