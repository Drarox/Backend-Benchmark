using Microsoft.AspNetCore.Mvc;

var builder = WebApplication.CreateBuilder(args);

var app = builder.Build();

app.MapPost("/process", ([FromBody] NumbersInput input) =>
{
    var result = input.Numbers.Select(x => x * x).Sum();
    return new ResultOutput(result);
});

app.Run();

public record NumbersInput(IEnumerable<int> Numbers);
public record ResultOutput(int Result);