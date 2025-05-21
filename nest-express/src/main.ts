import { NestFactory } from '@nestjs/core';
import { Module, Controller, Post, Body } from '@nestjs/common';

@Controller()
class AppController {
  @Post('process')
  process(@Body() body: { numbers: number[] }) {
    const result = body.numbers.reduce((sum, x) => sum + x * x, 0);
    return { result };
  }
}

@Module({ controllers: [AppController] })
class AppModule {}

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  await app.listen(3000);
}
bootstrap();
