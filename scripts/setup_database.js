import fs from 'fs';
import path from 'path';
import dotenv from 'dotenv';
import pkg from 'pg';

dotenv.config({ path: '.env' });

const { Client } = pkg;

const client = new Client({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production' ? true : { rejectUnauthorized: false }
});

const migrationSql = fs.readFileSync(path.resolve('migrations/0000_initial_schema.sql'), 'utf8');

async function setupDatabase() {
  try {
    console.log('ð Conectando ao banco de dados...');
    await client.connect();
    console.log('â Conectado ao banco!');

    // Executar migraÃ§Ã£o
    console.log('\nð Executando migraÃ§Ã£o...');
    await client.query('BEGIN');
    await client.query(migrationSql);
    await client.query('COMMIT');
    console.log('â Tabelas criadas com sucesso!');

    // Inserir templates de documentos
    console.log('\nð Inserindo templates de documentos...');
    const templatesQuery = `
      INSERT INTO doc_templates (id, titulo, categoria, conteudo)
      VALUES 
        ('tpl-001', 'PetiÃ§Ã£o Inicial', 'Processos Civis', 'Modelo padrÃ£o de petiÃ§Ã£o inicial para aÃ§Ã£o cÃ­vel'),
        ('tpl-002', 'ContestaÃ§Ã£o', 'Processos Civis', 'Modelo padrÃ£o de contestaÃ§Ã£o'),
        ('tpl-003', 'Recurso de ApelaÃ§Ã£o', 'Recursos', 'Modelo padrÃ£o de recurso de apelaÃ§Ã£o'),
        ('tpl-004', 'Parecer JurÃ­dico', 'Pareceres', 'Modelo padrÃ£o de parecer jurÃ­dico'),
        ('tpl-005', 'Contrato de PrestaÃ§Ã£o de ServiÃ§os', 'Contratos', 'Modelo padrÃ£o de contrato de serviÃ§os')
      ON CONFLICT DO NOTHING;
    `;
    await client.query(templatesQuery);
    console.log('â Templates de documentos inseridos!');

    // Inserir usuÃ¡rios (advogados)
    console.log('\nð¨ââï¸ Inserindo usuÃ¡rios (advogados)...');
    const usersQuery = `
      INSERT INTO users (id, username, password)
      VALUES 
        ('user-001', 'advogado1', 'senha123'),
        ('user-002', 'advogado2', 'senha456'),
        ('user-003', 'admin_oab', 'admin123')
      ON CONFLICT DO NOTHING;
    `;
    await client.query(usersQuery);
    console.log('â UsuÃ¡rios (advogados) inseridos!');

    // Verificar dados
    console.log('\nð Verificando dados inseridos...');
    
    const templatesRes = await client.query('SELECT * FROM doc_templates;');
    console.log(`\nð Templates encontrados: ${templatesRes.rows.length}`);
    templatesRes.rows.forEach(row => {
      console.log(`   - ${row.titulo} (${row.categoria})`);
    });

    const usersRes = await client.query('SELECT id, username FROM users;');
    console.log(`\nð¨ââï¸ UsuÃ¡rios encontrados: ${usersRes.rows.length}`);
    usersRes.rows.forEach(row => {
      console.log(`   - ${row.username} (ID: ${row.id})`);
    });

    console.log('\nâ Setup do banco de dados concluÃ­do com sucesso!');
    console.log('\nð Resumo:');
    console.log('   â 13 tabelas criadas');
    console.log(`   â ${templatesRes.rows.length} templates de documentos inseridos`);
    console.log(`   â ${usersRes.rows.length} usuÃ¡rios registrados`);

    await client.end();
    process.exit(0);
  } catch (err) {
    console.error('\nâ Erro:', err.message);
    console.error(err.stack);
    try {
      await client.query('ROLLBACK');
    } catch (e) {
      // Ignore rollback errors
    }
    await client.end();
    process.exit(1);
  }
}

setupDatabase();
