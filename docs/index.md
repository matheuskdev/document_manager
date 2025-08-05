# Bem-vindo à Documentação do Document Manager

Document Manager é um sistema robusto e eficiente de gerenciamento de documentos, construído com Python, Django e uma arquitetura limpa. Nosso principal objetivo é fornecer uma plataforma segura e escalável para a criação, organização e gestão de diferentes tipos de documentos, como contratos e protocolos.

Esta documentação foi criada para ajudar desenvolvedores, administradores e usuários a entenderem a fundo a arquitetura, as funcionalidades e a forma de interagir com o sistema.

---

### 🚀 Começando

Se você é um desenvolvedor novo no projeto, comece por aqui para entender a estrutura e como configurar o ambiente de desenvolvimento.

- **[Instalação e Configuração](getting-started/installation.md):** Guia passo a passo para configurar o ambiente, instalar dependências e rodar a aplicação localmente.
- **[Visão Geral da Arquitetura](getting-started/architecture.md):** Uma explanação detalhada sobre a arquitetura limpa do projeto, suas camadas e como elas se comunicam.
- **[Estrutura do Projeto](getting-started/project-structure.md):** Um mapa completo dos diretórios e arquivos do projeto.

---

### 📚 Entendendo a Arquitetura Limpa

Nossa aplicação foi projetada com base em princípios de arquitetura limpa (Clean Architecture) para garantir escalabilidade, testabilidade e separação de responsabilidades.

- **[Domínio (Domain)](architecture/domain.md):** Onde reside a lógica de negócio principal, com entidades como `Document` e `Tenant`, e a definição de repositórios.
- **[Aplicação (Application)](architecture/application.md):** A camada que orquestra o fluxo de dados com os Casos de Uso (Use Cases) e DTOs.
- **[Infraestrutura (Infrastructure)](architecture/infrastructure.md):** A camada de detalhes, que implementa a persistência de dados com Django ORM, as views e as APIs.
- **[Testes (Tests)](architecture/tests.md):** Guia sobre como a abordagem de arquitetura limpa facilita a escrita de testes unitários robustos e isolados.

---

### 📑 Funcionalidades Principais

Aqui você encontrará a documentação completa sobre as funcionalidades do sistema e como utilizá-las.

- **[Gerenciamento de Documentos](features/document-management.md):** Explica como criar, visualizar, editar e deletar diferentes tipos de documentos.
- **[Módulo de Contratos](features/contracts.md):** Documentação específica sobre a entidade `Contract` e suas regras de negócio, como renovação automática e status.
- **[Multi-empresa (Multi-tenant)](features/multi-tenant.md):** Como o sistema foi projetado para funcionar de forma segura com múltiplos tenants (empresas e filiais).

---

### ⚙️ Referência Técnica

- **[API RESTful](api/rest.md):** Documentação da API, endpoints e exemplos de requisições.
- **[Eventos de Domínio](technical/domain-events.md):** Uma explicação sobre como e por que utilizamos eventos de domínio para gerenciar a comunicação entre as partes do sistema.
- **[Decisões de Design](technical/design-decisions.md):** Um registro das principais decisões de design e arquitetura tomadas durante o desenvolvimento.

---

### 🤝 Contribuições

Quer ajudar a melhorar o projeto? Ótimo! Leia nosso [guia de contribuição](contributing.md) para saber como começar.

Se tiver dúvidas, sugestões ou encontrar um bug, por favor, abra uma `issue` no nosso repositório no GitHub.