package main

import (
	"encoding/json"
	"io"
	"net/http"
)

type Input struct {
	Numbers []int `json:"numbers"`
}

func handler(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" && r.URL.Path == "/process" {
		var input Input
		body, _ := io.ReadAll(r.Body)
		json.Unmarshal(body, &input)
		sum := 0
		for _, n := range input.Numbers {
			sum += n * n
		}
		response, _ := json.Marshal(map[string]int{"result": sum})
		w.Header().Set("Content-Type", "application/json")
		w.Write(response)
	}
}

func main() {
	http.HandleFunc("/process", handler)
	http.ListenAndServe(":3000", nil)
}
