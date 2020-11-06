import { Component } from '@angular/core';

@Component({
//como se va a referir al componente
  selector: 'app-root',
  //indica donde esta el template
  templateUrl: './app.component.html',
  //indica donde esta la hoja de estilo
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'web-angular';
}
