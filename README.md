# Assistente JurÃ­dico com RobÃ´ JurÃ­dico Integrado

Este projeto combina um assistente jurÃ­dico com um robÃ´ de monitoramento jurÃ­dico, criando uma plataforma completa para automaÃ§Ã£o de tarefas jurÃ­dicas.

Desenvolvido por **Maikon da Rocha Caldeira** - Manhumirim, MG

## RobÃ´ JurÃ­dico

O robÃ´ jurÃ­dico Ã© uma funcionalidade integrada que automatiza o monitoramento de publicaÃ§Ãµes jurÃ­dicas e a comunicaÃ§Ã£o com clientes. Ele realiza as seguintes tarefas:

- Consulta automaticamente a API do DJEN/CNJ para novas publicaÃ§Ãµes
- Identifica quais clientes sÃ£o afetados por cada publicaÃ§Ã£o
- Extrai datas importantes e prazos das publicaÃ§Ãµes
- Cria rascunhos de e-mails no Gmail para notificar os clientes
- Opcionalmente, salva os documentos no Google Drive

### Como usar

1. Configure as variÃ¡veis de ambiente no arquivo `.env` (veja `.env.example`)
2. Prepare a planilha de clientes (`clientes.xlsx`)
3. Acesse a interface web e vÃ¡ atÃ© a seÃ§Ã£o do RobÃ´ JurÃ­dico
4. Verifique o status de configuraÃ§Ã£o
5. Execute o robÃ´ manualmente ou agende execuÃ§Ãµes automÃ¡ticas

Para mais detalhes, consulte a [documentaÃ§Ã£o completa do robÃ´ jurÃ­dico](docs/robo-juridico.md).

## ð Sobre o Projeto

Este projeto reÃºne **duas funcionalidades principais** em uma Ãºnica aplicaÃ§Ã£o web PWA (Progressive Web App):

### 1ï¸â£ HTML Playground
Editor de cÃ³digo HTML ao vivo com visualizaÃ§Ã£o em tempo real.
- Cole seu cÃ³digo HTML, CSS e JavaScript
- Veja o resultado instantaneamente no preview
- Editor com syntax highlighting
- Suporte a mÃºltiplas fontes e temas
- Funciona offline (PWA)

### 2ï¸â£ Assistente JurÃ­dico com IA
Assistente jurÃ­dico inteligente alimentado por IA (Google Gemini).
- Consultas jurÃ­dicas em linguagem natural
- Comparador de documentos jurÃ­dicos
- Consulta processual
- Auditoria financeira
- Painel de processos
- TramitaÃ§Ã£o e filtrador jurÃ­dico
- MÃ³dulo previdenciÃ¡rio

---

## ð Tecnologias Utilizadas

- **Frontend:** React 18 + TypeScript + Vite
- **Roteamento:** Wouter
- **UI:** Tailwind CSS + Radix UI + shadcn/ui
- **Editor de CÃ³digo:** TinyMCE + TipTap
- **IA:** Google Gemini API + OpenAI
- **Backend:** Express.js (Node.js)
- **PWA:** Service Worker + Web App Manifest
- **Banco de Dados:** PostgreSQL + Drizzle ORM
- **AutenticaÃ§Ã£o:** Passport.js + JWT

---

## ð¦ InstalaÃ§Ã£o e ExecuÃ§Ã£o

```bash
# Instalar dependÃªncias
npm install

# Modo desenvolvimento
npm run dev

# Build para produÃ§Ã£o
npm run build

# Iniciar em produÃ§Ã£o
npm start
```

---

## ðï¸ Estrutura do Projeto

```
âââ client/
â   âââ src/
â   â   âââ pages/           # PÃ¡ginas da aplicaÃ§Ã£o
â   â   â   âââ playground.tsx          # HTML Playground
â   â   â   âââ legal-assistant.tsx     # Assistente JurÃ­dico
â   â   â   âââ comparador-juridico.tsx # Comparador de documentos
â   â   â   âââ consulta-processual.tsx # Consulta processual
â   â   â   âââ auditoria-financeira.tsx
â   â   â   âââ painel-processos.tsx
â   â   â   âââ tramitacao.tsx
â   â   â   âââ filtrador.tsx
â   â   â   âââ previdenciario.tsx
â   â   âââ components/      # Componentes reutilizÃ¡veis
â   â   âââ hooks/           # Custom hooks
â   â   âââ lib/             # UtilitÃ¡rios
â   âââ public/
â       âââ manifest.json    # PWA manifest
â       âââ sw.js            # Service Worker
â       âââ tinymce/         # Editor TinyMCE local
âââ server/                  # Backend Express
âââ shared/                  # Tipos e schemas compartilhados
âââ package.json
```

---

## ð Rotas da AplicaÃ§Ã£o

| Rota | Funcionalidade |
|------|---------------|
| `/` | Assistente JurÃ­dico (pÃ¡gina inicial) |
| `/playground` | HTML Playground |
| `/comparador` | Comparador JurÃ­dico |
| `/consulta` | Consulta Processual |
| `/auditoria` | Auditoria Financeira |
| `/painel` | Painel de Processos |
| `/tramitacao` | TramitaÃ§Ã£o |
| `/filtrador` | Filtrador JurÃ­dico |
| `/previdenciario` | MÃ³dulo PrevidenciÃ¡rio |
| `/token` | Gerador de Token |

---

## ð± PWA (Progressive Web App)

O projeto funciona como PWA instalÃ¡vel em dispositivos mÃ³veis e desktop:
- â Funciona offline (Service Worker)
- â InstalÃ¡vel na tela inicial
- â Ãcones personalizados (192x192 e 512x512)
- â Tema de cor configurado (`#6366f1`)

---

## âï¸ Autor

**Maikon da Rocha Caldeira**  
Manhumirim - MG, Brasil

---

## ð LicenÃ§a

MIT
