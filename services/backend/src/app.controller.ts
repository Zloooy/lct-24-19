import { Body, Controller, Get, Put } from '@nestjs/common';
import { ApiOperation } from '@nestjs/swagger';
import { AppService } from './app.service';
import { AppConfig, AppConfigService } from './app-config/app-config.service';

@Controller('/v1/app')
export class AppController {
  constructor(
    private readonly appService: AppService,
    private readonly appConfigService: AppConfigService,
  ) {}

  @Get()
  getHello(): string {
    return this.appService.getHello();
  }

  @ApiOperation({ operationId: 'getConfig' })
  @Get('/config')
  getConfig() {
    return this.appConfigService.getConfig();
  }

  @ApiOperation({ operationId: 'setConfig' })
  @Put('/config')
  setConfig(@Body() data: AppConfig) {
    this.appConfigService.setConfig(data);
    return {};
  }
}
