package com.example.spring_boot;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class ProcessController {

    public static class ProcessRequest {
        private List<Integer> numbers;

        public List<Integer> getNumbers() {
            return numbers;
        }

        public void setNumbers(List<Integer> numbers) {
            this.numbers = numbers;
        }
    }

    public static class ProcessResponse {
        private long result;

        public ProcessResponse(long result) {
            this.result = result;
        }

        public long getResult() {
            return result;
        }

        public void setResult(long result) {
            this.result = result;
        }
    }

    @PostMapping("/process")
    public ProcessResponse process(@RequestBody ProcessRequest request) {
        long sumOfSquares = request.getNumbers().stream()
                .mapToLong(n -> (long) n * n)
                .sum();
        return new ProcessResponse(sumOfSquares);
    }
}
