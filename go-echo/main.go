package main

import (
    "net/http"
    "github.com/labstack/echo/v4"
)

type Input struct {
    Numbers []int `json:"numbers"`
}

func main() {
    e := echo.New()
    e.POST("/process", func(c echo.Context) error {
        input := new(Input)
        if err := c.Bind(input); err != nil {
            return c.JSON(http.StatusBadRequest, map[string]string{"error": "Invalid JSON"})
        }
        sum := 0
        for _, n := range input.Numbers {
            sum += n * n
        }
        return c.JSON(http.StatusOK, map[string]int{"result": sum})
    })
    e.Start(":3000")
}
