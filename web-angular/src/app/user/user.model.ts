export interface IUser {
    userId: number;
    email: string;
    password: string;
    admin: boolean;
    sensors: number;
}

export class User implements IUser{
    constructor(
        public userId: number,
        public email: string,
        public password: string,
        public admin: boolean,
        public sensors: number){}
}
