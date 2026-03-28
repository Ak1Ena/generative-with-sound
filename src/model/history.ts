import { Column, Entity } from "typeorm";
import { Model } from "./generic/model";
import { ClientType } from "../type/client";

@Entity()
export class History extends Model{
    @Column()
    message?: string

    @Column({
        type:'enum',
        enum: ClientType
    })
    client?: string
} 