import { Component, OnInit } from '@angular/core';
//importar modelo sensor
import {User} from './sensor.model'

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
      id_num : 1,
    },
    {
      name: 'SENSBD2',
      active: true,
      status: true,
      id_num : 2,
    },
  {
      name: "SENSVF3",
      active: true,
      status: false,
      id_num : 3,
    },
    {
      name: 'SENSJJH',
      active: true,
      status: true,
      id_num : 5,
    },
    {
      name: 'SENSYO9',
      active: false,
      status: true,
      id_num : 4,
    },

  ];
  constructor() { }

  ngOnInit(): void {
  }

}
