import { User } from "../user/user.model";

export interface Isensor{
    sensorId: number;
    name: string;
    status: boolean;
    active: boolean;
    ip?: number;
    port?: number;
    user?: User;
    userId?: number;
}

export class Sensor implements Isensor{
    constructor(
        public sensorId: number,
        public name: string,
        public status: boolean,
        public active: boolean,
        public ip?: number,
        public port?: number,
        public user?: User,
        public userId?: number
    ){}

}
