import { DataSource } from "typeorm";
import { SnakeNamingStrategy } from 'typeorm-naming-strategies'

export const dataSources = new Map<string, DataSource>()
const entities = ['src/model/*.ts']
const migrations = ['src/migrations/*.js']

export const dataSource = new DataSource({
  type: 'postgres',
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT || '5432'),
  username: process.env.DB_USERNAME || 'postgres',
  password: process.env.DB_PASSWORD || 'password',
  database: process.env.DB_DATABASE || 'postgres',
  entities,
  migrations,
  migrationsRun: false,
  logging: false,
  namingStrategy: new SnakeNamingStrategy(),
})

const runMigrations = (migrationsRun: boolean) => async (ds: DataSource) => {
  if (migrationsRun) {
    const options: { transaction?: "all" | "none" | "each" } = {};
    if (ds.options.migrationsTransactionMode) {
      options.transaction = ds.options.migrationsTransactionMode;
    }
    await ds.runMigrations(options);
  }
  return ds
}

export const initialize = (migrationsRun = true) =>
  new Promise<DataSource>((res) => {
    const connect = () =>
      dataSource
        .initialize()
        .then(runMigrations(migrationsRun))
        .then(res)
        .catch((err) => {
          if (dataSource.isInitialized) dataSource.destroy()
          setTimeout(() => connect(), 3000)
        })
    connect()
  })

export const destroy = async () => {
  for (const [id, ds] of dataSources.entries()) {
    const logId = id.substring(0, 8)
    await ds.destroy()
  }
  await dataSource.destroy()
}