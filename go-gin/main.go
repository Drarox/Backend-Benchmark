package main

import (
	"github.com/gin-gonic/gin"
	"io"
	"net/http"
)

type Input struct {
	Numbers []int `json:"numbers"`
}

func main() {
	gin.SetMode(gin.ReleaseMode)
	gin.DefaultWriter = io.Discard

	r := gin.Default()
	r.POST("/process", func(c *gin.Context) {
		var input Input
		if err := c.ShouldBindJSON(&input); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid JSON"})
			return
		}
		sum := 0
		for _, n := range input.Numbers {
			sum += n * n
		}
		c.JSON(200, gin.H{"result": sum})
	})
	r.Run(":3000")
}
