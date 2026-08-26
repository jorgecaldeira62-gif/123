/**
 * run-migration.cjs
 * Executa a migration inicial do Drizzle manualmente via postgres.js
 *
 * Uso:
 *   node scripts/run-migration.cjs
 *
 * PrÃ©-requisito: DATABASE_URL definida em .env (ou no ambiente)
 */

'use strict';

const path  = require('path');
const fs    = require('fs');

// Carrega o .env da raiz do projeto antes de qualquer coisa
require('dotenv').config({ path: path.resolve(__dirname, '../.env') });

if (!process.env.DATABASE_URL) {
  console.error('â  DATABASE_URL nÃ£o encontrada. Verifique o .env.');
  process.exit(1);
}

// ââ DependÃªncias ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
const postgres = require('postgres');

// ââ ConexÃ£o âââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
const sql = postgres(process.env.DATABASE_URL, {
  ssl: 'require',   // Neon exige SSL
  max: 1,           // uma Ãºnica conexÃ£o Ã© suficiente para migrations
});

// ââ Leitura do arquivo SQL âââââââââââââââââââââââââââââââââââââââââââââââââââ
const migrationPath = path.resolve(__dirname, '../migrations/0000_initial_schema.sql');

if (!fs.existsSync(migrationPath)) {
  console.error('â  Arquivo de migration nÃ£o encontrado:', migrationPath);
  process.exit(1);
}

const migrationSql = fs.readFileSync(migrationPath, 'utf8');

// ââ ExecuÃ§Ã£o âââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
(async () => {
  try {
    console.log('ð  Iniciando migration inicial...\n');

    // Executa todo o DDL dentro de uma transaÃ§Ã£o
    await sql.begin(async (tx) => {
      // postgres.js aceita strings brutas via sql.unsafe() dentro de transaÃ§Ãµes
      await tx.unsafe(migrationSql);
    });

    console.log('â  DDL executado â tabelas criadas/verificadas com sucesso.\n');

    // ââ Tabela de controle do Drizzle ââââââââââââââââââââââââââââââââââââââââ
    // Drizzle usa "drizzle"."__drizzle_migrations" (schema "drizzle")
    await sql`
      CREATE SCHEMA IF NOT EXISTS "drizzle"
    `;

    await sql`
      CREATE TABLE IF NOT EXISTS "drizzle"."__drizzle_migrations" (
        "id"         serial      PRIMARY KEY,
        "hash"       varchar(191) NOT NULL,
        "created_at" bigint
      )
    `;

    // Insere somente se ainda nÃ£o existir (idempotente)
    const existing = await sql`
      SELECT 1 FROM "drizzle"."__drizzle_migrations"
      WHERE hash = 'initial'
      LIMIT 1
    `;

    if (existing.length === 0) {
      await sql`
        INSERT INTO "drizzle"."__drizzle_migrations" (hash, created_at)
        VALUES ('initial', ${BigInt(Date.now())})
      `;
      console.log('ð  Migration registrada na tabela de controle.');
    } else {
      console.log('â¹ï¸   Migration "initial" jÃ¡ estava registrada â nada inserido.');
    }

    // ââ ValidaÃ§Ã£o rÃ¡pida âââââââââââââââââââââââââââââââââââââââââââââââââââââ
    const [{ count }] = await sql`SELECT COUNT(*)::int AS count FROM users`;
    console.log(`\nð  Tabela "users" acessÃ­vel â registros actuais: ${count}`);

    console.log('\nâ  Banco pronto!');
  } catch (err) {
    console.error('\nâ  Erro durante a migration:');
    console.error('    ', err.message);
    process.exitCode = 1;
  } finally {
    await sql.end();
  }
})();
