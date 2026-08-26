const { Client } = require('pg');

// Get the database connection details from environment variables
const client = new Client({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false }
});

(async () => {
  try {
    await client.connect();
    console.log('â ConexÃ£o com o banco de dados bem-sucedida!');
    
    // Test a simple query
    const result = await client.query('SELECT version()');
    console.log('VersÃ£o do PostgreSQL:', result.rows[0].version);
    
    await client.end();
    console.log('ð ConexÃ£o encerrada.');
  } catch (err) {
    console.error('â Erro na conexÃ£o:', err.message);
    await client.end();
  }
})();