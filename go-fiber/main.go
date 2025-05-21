package main

import (
    "github.com/gofiber/fiber/v2"
)

type Input struct {
    Numbers []int `json:"numbers"`
}

func main() {
    app := fiber.New()

    app.Post("/process", func(c *fiber.Ctx) error {
        input := new(Input)
        if err := c.BodyParser(input); err != nil {
            return c.Status(400).JSON(fiber.Map{"error": "Invalid JSON"})
        }
        sum := 0
        for _, n := range input.Numbers {
            sum += n * n
        }
        return c.JSON(fiber.Map{"result": sum})
    })

    app.Listen(":3000")
}
