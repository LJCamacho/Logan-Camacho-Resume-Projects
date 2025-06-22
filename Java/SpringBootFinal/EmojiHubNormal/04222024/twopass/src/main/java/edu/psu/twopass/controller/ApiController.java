package edu.psu.twopass.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class ApiController {

    @GetMapping("/api")
    public List<String> api() {
        return List.of("Hello", "World");
    }
}
