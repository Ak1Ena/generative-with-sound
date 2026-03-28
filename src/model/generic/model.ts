import {
  CreateDateColumn,
  DeleteDateColumn,
  Index,
  PrimaryGeneratedColumn,
  UpdateDateColumn,
} from 'typeorm'
import { defaultDateOptions } from './dateColumn'

/**
 * Base model for timestamps metadata and uuid
 */
export abstract class Model {
  @PrimaryGeneratedColumn('uuid')
  id!: string

  @CreateDateColumn(defaultDateOptions)
  createdAt!: Date
  @UpdateDateColumn(defaultDateOptions)
  updatedAt!: Date
  @Index()
  @DeleteDateColumn(defaultDateOptions)
  deletedAt!: Date | null
}