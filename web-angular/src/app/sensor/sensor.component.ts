import { Component, OnInit } from '@angular/core';
//importar modelo sensor
import {Sensor} from './sensor.model'

@Component({
  selector: 'app-sensor',
  templateUrl: './sensor.component.html',
  styleUrls: ['./sensor.component.scss']
})
export class SensorComponent implements OnInit {
  selectedSensor: Sensor;
  sensors: Sensor[]=[
    {
      name: 'SENSAD1',
      active: true,
      status: true,
      sensorId : 1,
    },
    {
      name: 'SENSBD2',
      active: true,
      status: true,
      sensorId : 2,
    },
  {
      name: "SENSVF3",
      active: true,
      status: false,
      sensorId : 3,
    },
    {
      name: 'SENSJJH',
      active: true,
      status: true,
      sensorId : 5,
    },
    {
      name: 'SENSYO9',
      active: false,
      status: true,
      sensorId : 4,
    },

  ];
  constructor() { }

  ngOnInit(): void {
  }
  //funcion para cargar el sensor seleccionado a la variable selectSensor
  onSelect(sensor:Sensor): void{
    this.selectedSensor=sensor;
  }


}
