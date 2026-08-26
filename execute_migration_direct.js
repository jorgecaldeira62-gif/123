const fs = require('fs');
const { Client } = require('pg');

// Load environment variables
const envPath = 'Live-Code-Runner/.env';
const envContent = fs.readFileSync(envPath, 'utf8');

// Parse environment variables
const envVars = {};
envContent.split('\n').forEach(line => {
  if (line.trim() && !line.startsWith('#') && line.includes('=')) {
    const [key, ...value] = line.split('=');
    envVars[key.trim()] = value.join('=').trim().replace(/^"(.*)"$/, '$1');
  }
});

// Create database client
const client = new Client({
  connectionString: envVars.DATABASE_URL,
  ssl: { rejectUnauthorized: false }
});

// Read migration file
const migrationSql = fs.readFileSync('migrations/0000_initial_schema.sql', 'utf8');

(async () => {
  try {
    await client.connect();
    console.log('ð Conectado ao banco...');
    
    await client.query('BEGIN');
    await client.query(migrationSql);
    await client.query('COMMIT');
    
    console.log('â 13 tabelas criadas!');
    
    // Test quick query
    const res = await client.query('SELECT 1 FROM users LIMIT 1');
    console.log('â ConexÃ£o com tabela users verificada!');
    
    await client.end();
    console.log('ð ConexÃ£o encerrada.');
    
  } catch (err) {
    await client.query('ROLLBACK');
    console.error('â Erro na migraÃ§Ã£o:', err.message);
    await client.end();
    process.exit(1);
  }
})();