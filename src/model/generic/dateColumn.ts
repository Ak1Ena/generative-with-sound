import { Column, type ColumnOptions } from 'typeorm'

export const defaultDateOptions: ColumnOptions = {
  type: 'timestamptz',
  precision: 3,
}

/**
 * This decorator adds the timestamptz type with precision 3.
 */
export const DateColumn = (options: ColumnOptions = {}) =>
  Column({ ...defaultDateOptions, ...options })