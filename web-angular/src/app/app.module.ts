import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { SensorComponent } from './sensor/sensor.component';
import { SeismComponent } from './seism/seism.component';
import { UserComponent } from './user/user.component';
import { SensorDetailComponent } from './sensor/sensor-detail/sensor-detail.component';

@NgModule({
  declarations: [
    AppComponent,
    SensorComponent,
    SeismComponent,
    UserComponent,
    SensorDetailComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
