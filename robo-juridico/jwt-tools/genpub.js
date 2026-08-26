const fs = require('fs');
const { createPublicKey } = require('crypto');

// âââ Uso: node genpub.js [caminho/chave_privada.pem] âââââââââââââââââââââââââ
// Gera a chave pÃºblica (.pub.pem) a partir da chave privada RSA.
// A chave pÃºblica deve ser enviada para o PDPJ no processo de registro.

const privPath = process.argv[2] || 'chave_privada.pem';

if (!fs.existsSync(privPath)) {
  console.error('â Arquivo de chave privada nÃ£o encontrado:', privPath);
  console.error('   Passe o caminho como: node genpub.js "C:/caminho/chave_privada.pem"');
  process.exit(1);
}

try {
  const priv = fs.readFileSync(privPath, 'utf8');
  const pub  = createPublicKey(priv).export({ type: 'spki', format: 'pem' });
  const outFile = 'maikon.pub.pem';
  fs.writeFileSync(outFile, pub);
  console.log(`â Chave pÃºblica gerada: ${outFile}`);
  console.log('   â Envie este arquivo ao PDPJ para registro da chave.');
} catch (err) {
  console.error('â Erro ao gerar chave pÃºblica:', err.message);
  process.exit(1);
}
